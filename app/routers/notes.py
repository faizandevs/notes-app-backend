# app/routers/notes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas
from app.database import SessionLocal
from app.routers.auth import get_current_user
from app.services import note_service
from app.utils import analyze_sentiment
router = APIRouter(prefix="/notes", tags=["notes"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def note_with_sentiment(note):
    sentiment = analyze_sentiment(note.description or "")
    return {
        "id": note.id,
        "title": note.title,
        "description": note.description,
        "owner_id": note.owner_id,
        "sentiment": sentiment
    }
@router.get("/", response_model=List[schemas.NoteResponse])
def read_notes(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    notes = note_service.get_notes_for_user(db, current_user.id)
    return [note_with_sentiment(n) for n in notes]
@router.post("/", response_model=schemas.NoteResponse)
def create_note(note: schemas.NoteCreate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    created = note_service.create_note(db, note.title, note.description, current_user.id)
    return note_with_sentiment(created)


@router.get("/", response_model=List[schemas.NoteResponse])
def read_notes(db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return note_service.get_notes_for_user(db, current_user.id)

@router.get("/{note_id}", response_model=schemas.NoteResponse)
def read_note(note_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    return note_service.get_note_by_id_for_user(db, note_id, current_user.id)


@router.put("/{note_id}", response_model=schemas.NoteResponse)
def update_note(note_id: int, update: schemas.NoteUpdate, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    updated = note_service.update_note_for_user(db, note_id, current_user.id, title=update.title, description=update.description)
    return note_with_sentiment(updated)
@router.delete("/{note_id}")
def delete_note(note_id: int, db: Session = Depends(get_db), current_user = Depends(get_current_user)):
    note_service.delete_note_for_user(db, note_id, current_user.id)
    return {"detail": f"Note {note_id} deleted"}
