# app/main.py
 
import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app import models
from app.routers import auth as auth_router, notes as notes_router
from app.exceptions import NotFoundError, ForbiddenError, BadRequestError
from dotenv import load_dotenv
load_dotenv()
# create tables if missing (dev convenience)
Base.metadata.create_all(bind=engine)

# basic logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Notes API")
# Allow frontend origin
origins = [
    "http://localhost:5173",   # Vite dev server
    "http://127.0.0.1:5173",
    "http://localhost:3000",   # React default port
    "http://127.0.0.1:3000",
    "https://notes-app-backend-54zl.onrender.com"  # your deployed backend
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# include routers
app.include_router(auth_router.router)
app.include_router(notes_router.router)


# Global exception handlers (consistent JSON responses)
@app.exception_handler(NotFoundError)
async def not_found_handler(request: Request, exc: NotFoundError):
    return JSONResponse(status_code=404, content={"error": str(exc)})

@app.exception_handler(ForbiddenError)
async def forbidden_handler(request: Request, exc: ForbiddenError):
    return JSONResponse(status_code=403, content={"error": str(exc)})

@app.exception_handler(BadRequestError)
async def bad_request_handler(request: Request, exc: BadRequestError):
    return JSONResponse(status_code=400, content={"error": str(exc)})

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    # log full exception for operators, but return safe message to clients
    logger.exception("Unhandled exception: %s", exc)
    return JSONResponse(status_code=500, content={"error": "Internal server error"})
