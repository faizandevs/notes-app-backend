# app/services/note_service.py
from sqlalchemy.orm import Session
from app import models
from app.exceptions import NotFoundError

def create_note(db: Session, title: str, description: str, owner_id: int) -> models.NoteDB:
    note = models.NoteDB(title=title, description=description, owner_id=owner_id)
    db.add(note)
    db.commit()
    db.refresh(note)
    return note


def get_notes_for_user(db: Session, user_id: int):
    return db.query(models.NoteDB).filter(models.NoteDB.owner_id == user_id).all()


def get_note_by_id_for_user(db: Session, note_id: int, user_id: int):
    note = db.query(models.NoteDB).filter(
        models.NoteDB.id == note_id,
        models.NoteDB.owner_id == user_id
    ).first()
    if not note:
        raise NotFoundError("Note not found")
    return note


def update_note_for_user(db: Session, note_id: int, user_id: int, title: str = None, description: str = None):
    note = db.query(models.NoteDB).filter(
        models.NoteDB.id == note_id, models.NoteDB.owner_id == user_id
    ).first()
    if not note:
        raise NotFoundError("Note not found")

    if title is not None:
        note.title = title
    if description is not None:
        note.description = description

    db.commit()
    db.refresh(note)
    return note


def delete_note_for_user(db: Session, note_id: int, user_id: int):
    note = db.query(models.NoteDB).filter(
        models.NoteDB.id == note_id, models.NoteDB.owner_id == user_id
    ).first()
    if not note:
        raise NotFoundError("Note not found")

    db.delete(note)
    db.commit()
    return note
