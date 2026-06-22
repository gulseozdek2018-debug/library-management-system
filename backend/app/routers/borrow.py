from datetime import datetime, timedelta
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..auth import get_current_user

router = APIRouter(tags=["Borrow"])


@router.post("/borrow", response_model=schemas.BorrowTransactionResponse)
def borrow_book(
    borrow_data: schemas.BorrowCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    book = db.query(models.Book).filter(models.Book.isbn == borrow_data.isbn).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book.available_copies <= 0:
        raise HTTPException(status_code=400, detail="Book is not available")

    existing_transaction = db.query(models.BorrowTransaction).filter(
        models.BorrowTransaction.user_id == current_user.id,
        models.BorrowTransaction.isbn == borrow_data.isbn,
        models.BorrowTransaction.status == "borrowed"
    ).first()

    if existing_transaction:
        raise HTTPException(status_code=400, detail="You already borrowed this book")

    borrow_date = datetime.utcnow()
    due_date = borrow_date + timedelta(days=borrow_data.days)

    transaction = models.BorrowTransaction(
        user_id=current_user.id,
        isbn=borrow_data.isbn,
        borrow_date=borrow_date,
        due_date=due_date,
        status="borrowed"
    )

    book.available_copies -= 1

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    return transaction


@router.post("/return", response_model=schemas.BorrowTransactionResponse)
def return_book(
    return_data: schemas.ReturnBookRequest,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    transaction = db.query(models.BorrowTransaction).filter(
        models.BorrowTransaction.transaction_id == return_data.transaction_id,
        models.BorrowTransaction.user_id == current_user.id,
        models.BorrowTransaction.status == "borrowed"
    ).first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Active borrow transaction not found")

    book = db.query(models.Book).filter(models.Book.isbn == transaction.isbn).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    transaction.return_date = datetime.utcnow()
    transaction.status = "returned"
    book.available_copies += 1

    db.commit()
    db.refresh(transaction)

    return transaction


@router.get("/borrow/history", response_model=List[schemas.BorrowTransactionResponse])
def borrow_history(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    transactions = db.query(models.BorrowTransaction).filter(
        models.BorrowTransaction.user_id == current_user.id
    ).all()

    return transactions