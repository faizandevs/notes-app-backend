# notesapi.py
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import models, schemas
from database import SessionLocal, engine
from auth import router as auth_router, get_current_user

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency: DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# include auth routes
app.include_router(auth_router)

# ---------- Notes ----------
@app.post("/notes/", response_model=schemas.NoteResponse)
def create_note(
    note: schemas.NoteCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_note = models.NoteDB(
        title=note.title,
        description=note.description,
        owner_id=current_user.id
    )
    db.add(db_note)
    db.commit()
    db.refresh(db_note)
    return db_note

@app.get("/notes/", response_model=List[schemas.NoteResponse])
def read_notes(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    return db.query(models.NoteDB).filter(models.NoteDB.owner_id == current_user.id).all()

@app.get("/notes/{note_id}", response_model=schemas.NoteResponse)
def read_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    note = db.query(models.NoteDB).filter(
        models.NoteDB.id == note_id,
        models.NoteDB.owner_id == current_user.id
    ).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note

@app.put("/notes/{note_id}", response_model=schemas.NoteResponse)
def update_note(
    note_id: int,
    update_data: schemas.NoteUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    note = db.query(models.NoteDB).filter(
        models.NoteDB.id == note_id,
        models.NoteDB.owner_id == current_user.id
    ).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    if update_data.title is not None:
        note.title = update_data.title
    if update_data.description is not None:
        note.description = update_data.description

    db.commit()
    db.refresh(note)
    return note

@app.delete("/notes/{note_id}")
def delete_note(
    note_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    note = db.query(models.NoteDB).filter(
        models.NoteDB.id == note_id,
        models.NoteDB.owner_id == current_user.id
    ).first()
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    db.delete(note)
    db.commit()
    return {"message": f"Note {note_id} deleted"}
