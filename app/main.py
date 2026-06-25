from fastapi import FastAPI
from app.api.auth import router as auth_router

from app.db.database import Base, engine
from app.models.user import User

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router, prefix="/auth", tags=["auth"])

@app.get("/")
def home():
    return {
        "message": "Auth Service Running"
    }