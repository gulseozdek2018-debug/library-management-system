from fastapi import FastAPI

app = FastAPI(title="Library Management System API")

@app.get("/")
def home():
    return {"message": "Library Management System API is running"}