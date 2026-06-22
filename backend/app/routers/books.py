from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import or_
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..auth import require_roles

router = APIRouter(prefix="/books", tags=["Books"])


@router.post("/", response_model=schemas.BookResponse)
def create_book(
    book: schemas.BookCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_roles("admin", "librarian"))
):
    existing_book = db.query(models.Book).filter(models.Book.isbn == book.isbn).first()

    if existing_book:
        raise HTTPException(status_code=400, detail="Book already exists")

    new_book = models.Book(**book.model_dump())

    db.add(new_book)
    db.commit()
    db.refresh(new_book)

    return new_book


@router.get("/", response_model=List[schemas.BookResponse])
def get_books(search: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Book)

    if search:
        search_text = f"%{search}%"
        query = query.filter(
            or_(
                models.Book.isbn.ilike(search_text),
                models.Book.title.ilike(search_text),
                models.Book.author.ilike(search_text),
                models.Book.publisher.ilike(search_text),
            )
        )

    return query.all()


@router.get("/{isbn}", response_model=schemas.BookResponse)
def get_book(isbn: str, db: Session = Depends(get_db)):
    book = db.query(models.Book).filter(models.Book.isbn == isbn).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return book


@router.put("/{isbn}", response_model=schemas.BookResponse)
def update_book(
    isbn: str,
    book_update: schemas.BookUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_roles("admin", "librarian"))
):
    book = db.query(models.Book).filter(models.Book.isbn == isbn).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    update_data = book_update.model_dump(exclude_unset=True)

    for key, value in update_data.items():
        setattr(book, key, value)

    db.commit()
    db.refresh(book)

    return book


@router.delete("/{isbn}")
def delete_book(
    isbn: str,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_roles("admin", "librarian"))
):
    book = db.query(models.Book).filter(models.Book.isbn == isbn).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    db.delete(book)
    db.commit()

    return {"message": "Book deleted successfully"}