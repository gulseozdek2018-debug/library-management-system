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

    existing_transaction = db.query(models.BorrowTransaction).filter(
        models.BorrowTransaction.user_id == current_user.id,
        models.BorrowTransaction.isbn == borrow_data.isbn,
        models.BorrowTransaction.status == "borrowed"
    ).first()

    if existing_transaction:
        raise HTTPException(status_code=400, detail="You already borrowed this book")

    if book.available_copies <= 0:
        raise HTTPException(status_code=400, detail="Book is not available. You can create a reservation.")

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

    # Fulfill any active/pending reservations for this user and book
    db.query(models.Reservation).filter(
        models.Reservation.user_id == current_user.id,
        models.Reservation.isbn == borrow_data.isbn,
        models.Reservation.status.in_(["active", "pending"])
    ).update({"status": "fulfilled"}, synchronize_session=False)

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
    query = db.query(models.BorrowTransaction).filter(
        models.BorrowTransaction.transaction_id == return_data.transaction_id
    )
    if current_user.role not in ["admin", "librarian"]:
        query = query.filter(models.BorrowTransaction.user_id == current_user.id)
    transaction = query.first()

    if not transaction:
        raise HTTPException(status_code=404, detail="Active borrow transaction not found")

    if transaction.status == "returned":
        raise HTTPException(status_code=400, detail="This book has already been returned")

    book = db.query(models.Book).filter(models.Book.isbn == transaction.isbn).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book.available_copies >= book.total_copies:
        raise HTTPException(status_code=400, detail="Available copies cannot exceed total copies")

    transaction.return_date = datetime.utcnow()
    transaction.status = "returned"
    book.available_copies += 1

    # Mark the oldest active/pending reservation for this book as fulfilled
    oldest_res = db.query(models.Reservation).filter(
        models.Reservation.isbn == transaction.isbn,
        models.Reservation.status.in_(["active", "pending"])
    ).order_by(models.Reservation.reservation_date.asc()).first()
    if oldest_res:
        oldest_res.status = "fulfilled"

    db.commit()
    db.refresh(transaction)

    return transaction


@router.get("/borrow/history", response_model=List[schemas.BorrowHistoryResponse])
def borrow_history(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    results = db.query(
        models.BorrowTransaction,
        models.Book.title,
        models.Book.author
    ).join(
        models.Book,
        models.Book.isbn == models.BorrowTransaction.isbn
    ).filter(
        models.BorrowTransaction.user_id == current_user.id
    ).order_by(
        models.BorrowTransaction.borrow_date.desc()
    ).all()

    history = []
    now = datetime.utcnow()
    for transaction, title, author in results:
        is_overdue = transaction.status == "borrowed" and transaction.due_date < now
        history.append({
            "transaction_id": transaction.transaction_id,
            "isbn": transaction.isbn,
            "title": title,
            "author": author,
            "borrow_date": transaction.borrow_date,
            "due_date": transaction.due_date,
            "return_date": transaction.return_date,
            "status": transaction.status,
            "overdue": is_overdue
        })

    return history