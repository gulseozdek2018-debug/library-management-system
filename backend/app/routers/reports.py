from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models
from ..database import get_db
from ..auth import require_roles

router = APIRouter(prefix="/reports", tags=["Reports"])


@router.get("/")
def get_reports_overview(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_roles("admin", "librarian"))
):
    total_books = db.query(models.Book).count()
    total_users = db.query(models.User).count()
    borrowed_books = db.query(models.BorrowTransaction).filter(
        models.BorrowTransaction.status == "borrowed"
    ).count()
    active_reservations = db.query(models.Reservation).filter(
        models.Reservation.status == "active"
    ).count()

    return {
        "total_books": total_books,
        "total_users": total_users,
        "currently_borrowed_books": borrowed_books,
        "active_reservations": active_reservations
    }


@router.get("/most-borrowed-books")
def most_borrowed_books(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_roles("admin", "librarian"))
):
    results = db.query(
        models.BorrowTransaction.isbn,
        models.Book.title,
        func.count(models.BorrowTransaction.transaction_id).label("borrow_count")
    ).join(
        models.Book,
        models.Book.isbn == models.BorrowTransaction.isbn
    ).group_by(
        models.BorrowTransaction.isbn,
        models.Book.title
    ).order_by(
        func.count(models.BorrowTransaction.transaction_id).desc()
    ).all()

    return [
        {
            "isbn": row.isbn,
            "title": row.title,
            "borrow_count": row.borrow_count
        }
        for row in results
    ]


@router.get("/active-users")
def active_users(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_roles("admin", "librarian"))
):
    results = db.query(
        models.User.id,
        models.User.username,
        models.User.email,
        models.User.role,
        func.count(models.BorrowTransaction.transaction_id).label("borrow_count")
    ).join(
        models.BorrowTransaction,
        models.User.id == models.BorrowTransaction.user_id
    ).group_by(
        models.User.id,
        models.User.username,
        models.User.email,
        models.User.role
    ).order_by(
        func.count(models.BorrowTransaction.transaction_id).desc()
    ).all()

    return [
        {
            "user_id": row.id,
            "username": row.username,
            "email": row.email,
            "role": row.role,
            "borrow_count": row.borrow_count
        }
        for row in results
    ]


@router.get("/borrowed-books")
def borrowed_books(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_roles("admin", "librarian"))
):
    results = db.query(models.BorrowTransaction).filter(
        models.BorrowTransaction.status == "borrowed"
    ).all()

    return [
        {
            "transaction_id": item.transaction_id,
            "user_id": item.user_id,
            "isbn": item.isbn,
            "borrow_date": item.borrow_date,
            "due_date": item.due_date,
            "status": item.status
        }
        for item in results
    ]


@router.get("/overdue-books")
def overdue_books(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_roles("admin", "librarian"))
):
    now = datetime.utcnow()

    results = db.query(models.BorrowTransaction).filter(
        models.BorrowTransaction.status == "borrowed",
        models.BorrowTransaction.due_date < now
    ).all()

    return [
        {
            "transaction_id": item.transaction_id,
            "user_id": item.user_id,
            "isbn": item.isbn,
            "borrow_date": item.borrow_date,
            "due_date": item.due_date,
            "status": item.status
        }
        for item in results
    ]


@router.get("/monthly-borrow-stats")
def monthly_borrow_stats(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(require_roles("admin", "librarian"))
):
    results = db.query(
        func.strftime("%Y-%m", models.BorrowTransaction.borrow_date).label("month"),
        func.count(models.BorrowTransaction.transaction_id).label("borrow_count")
    ).group_by(
        func.strftime("%Y-%m", models.BorrowTransaction.borrow_date)
    ).order_by(
        func.strftime("%Y-%m", models.BorrowTransaction.borrow_date)
    ).all()

    return [
        {
            "month": row.month,
            "borrow_count": row.borrow_count
        }
        for row in results
    ]