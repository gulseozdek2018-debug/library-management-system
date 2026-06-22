from fastapi import FastAPI

from .database import engine, Base
from . import models
from .routers import books

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management System API")

app.include_router(books.router)


@app.get("/")
def home():
    return {"message": "Library Management System API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}