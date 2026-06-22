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


@router.get("/", response_model=List[schemas.ReservationResponse])
def get_my_reservations(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    reservations = db.query(models.Reservation).filter(
        models.Reservation.user_id == current_user.id
    ).all()

    return reservations


@router.delete("/{reservation_id}")
def cancel_reservation(
    reservation_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    reservation = db.query(models.Reservation).filter(
        models.Reservation.reservation_id == reservation_id,
        models.Reservation.user_id == current_user.id,
        models.Reservation.status.in_(["active", "pending"])
    ).first()

    if not reservation:
        raise HTTPException(status_code=404, detail="Active reservation not found")

    reservation.status = "cancelled"

    db.commit()
    db.refresh(reservation)

    return {"message": "Reservation cancelled successfully"}