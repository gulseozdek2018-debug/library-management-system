from typing import Optional
from pydantic import BaseModel, ConfigDict


class BookCreate(BaseModel):
    isbn: str
    title: str
    author: str
    publisher: Optional[str] = None
    publication_year: Optional[int] = None
    total_copies: int = 1
    available_copies: int = 1


class BookUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    publication_year: Optional[int] = None
    total_copies: Optional[int] = None
    available_copies: Optional[int] = None


class BookResponse(BaseModel):
    isbn: str
    title: str
    author: str
    publisher: Optional[str] = None
    publication_year: Optional[int] = None
    total_copies: int
    available_copies: int

    model_config = ConfigDict(from_attributes=True)


class UserCreate(BaseModel):
    username: str
    email: str
    password: str
    role: str = "student"


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str

from datetime import datetime


class BorrowCreate(BaseModel):
    isbn: str
    days: int = 14


class ReturnBookRequest(BaseModel):
    transaction_id: int


class BorrowTransactionResponse(BaseModel):
    transaction_id: int
    user_id: int
    isbn: str
    borrow_date: datetime
    due_date: datetime
    return_date: Optional[datetime] = None
    status: str

    model_config = ConfigDict(from_attributes=True)