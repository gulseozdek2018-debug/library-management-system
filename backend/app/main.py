from fastapi import FastAPI
from .database import engine, Base
from . import models

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Library Management System API")


@app.get("/")
def home():
    return {"message": "Library Management System API is running"}


@app.get("/health")
def health_check():
    return {"status": "ok"}