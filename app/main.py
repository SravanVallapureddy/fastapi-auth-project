from fastapi import FastAPI
from app.api.auth import router as auth_router
from app.api.auth_controller import router as auth_controller_router
from app.api.upload_controller import router as upload_file_router

from app.db.database import Base, engine
from app.models.user import User

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(auth_controller_router, prefix="/api/v1/auth", tags=["auth-controller"])
app.include_router(upload_file_router, prefix="/api/v1/files", tags=["file-upload"])

@app.get("/")
def home():
    return {
        "message": "Auth Service Running"
    }