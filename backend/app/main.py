from fastapi import FastAPI

from .database import engine, Base
from . import models
from .routers import books, auth, borrow, reservations

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management System API")

app.include_router(books.router)
app.include_router(auth.router)
app.include_router(borrow.router)
app.include_router(reservations.router)


@app.get("/")
def home():
    return {"message": "Library Management System API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}