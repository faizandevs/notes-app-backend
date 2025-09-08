from fastapi import FastAPI
from app.database import engine
from app import models
from app.auth import router as auth_router
from app.notes import router as notes_router

# Create tables if they don't exist
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# include routers
app.include_router(auth_router)
app.include_router(notes_router)
