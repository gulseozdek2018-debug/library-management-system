from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..auth import get_current_user

router = APIRouter(prefix="/reservations", tags=["Reservations"])


@router.post("/", response_model=schemas.ReservationResponse)
def create_reservation(
    reservation_data: schemas.ReservationCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    book = db.query(models.Book).filter(models.Book.isbn == reservation_data.isbn).first()

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    if book.available_copies > 0:
        raise HTTPException(status_code=400, detail="Book is available, reservation is not needed")

    existing_reservation = db.query(models.Reservation).filter(
        models.Reservation.user_id == current_user.id,
        models.Reservation.isbn == reservation_data.isbn,
        models.Reservation.status.in_(["active", "pending"])
    ).first()

    if existing_reservation:
        raise HTTPException(status_code=400, detail="You already have an active or pending reservation for this book")

    reservation = models.Reservation(
        user_id=current_user.id,
        isbn=reservation_data.isbn,
        status="active"
    )

    db.add(reservation)
    db.commit()
    db.refresh(reservation)

    return reservation


@router.get("/", response_model=List[schemas.ReservationHistoryResponse])
def get_my_reservations(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(
        models.Reservation,
        models.Book.title,
        models.Book.author
    ).join(
        models.Book,
        models.Book.isbn == models.Reservation.isbn
    )
    if current_user.role not in ["admin", "librarian"]:
        query = query.filter(models.Reservation.user_id == current_user.id)

    results = query.order_by(models.Reservation.reservation_date.desc()).all()

    history = []
    for resv, title, author in results:
        history.append({
            "reservation_id": resv.reservation_id,
            "user_id": resv.user_id,
            "isbn": resv.isbn,
            "title": title,
            "author": author,
            "reservation_date": resv.reservation_date,
            "status": resv.status
        })

    return history


@router.delete("/{reservation_id}")
def cancel_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    query = db.query(models.Reservation).filter(
        models.Reservation.reservation_id == reservation_id,
        models.Reservation.status.in_(["active", "pending"])
    )
    if current_user.role not in ["admin", "librarian"]:
        query = query.filter(models.Reservation.user_id == current_user.id)

    reservation = query.first()

    if not reservation:
        raise HTTPException(status_code=404, detail="Active reservation not found")

    reservation.status = "cancelled"

    db.commit()
    db.refresh(reservation)

    return {"message": "Reservation cancelled successfully"}