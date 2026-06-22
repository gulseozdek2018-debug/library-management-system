from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from .database import Base


class Book(Base):
    __tablename__ = "books"

    isbn = Column(String, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=False)
    publisher = Column(String)
    publication_year = Column(Integer)
    total_copies = Column(Integer, default=1)
    available_copies = Column(Integer, default=1)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(String, default="member")


class BorrowTransaction(Base):
    __tablename__ = "borrow_transactions"

    transaction_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    isbn = Column(String, ForeignKey("books.isbn"), nullable=False)
    borrow_date = Column(DateTime, default=datetime.utcnow)
    due_date = Column(DateTime, nullable=False)
    return_date = Column(DateTime, nullable=True)
    status = Column(String, default="borrowed")


class Reservation(Base):
    __tablename__ = "reservations"

    reservation_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    isbn = Column(String, ForeignKey("books.isbn"), nullable=False)
    reservation_date = Column(DateTime, default=datetime.utcnow)
    status = Column(String, default="active")