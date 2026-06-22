from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from . import models
from .routers import books, auth, borrow, reservations, reports

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management System API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(books.router)
app.include_router(auth.router)
app.include_router(borrow.router)
app.include_router(reservations.router)
app.include_router(reports.router)


@app.get("/")
def home():
    return {"message": "Library Management System API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}