# app/schemas.py
from pydantic import BaseModel
from typing import Optional

# ---------- Notes ----------
class NoteBase(BaseModel):
    title: str
    description: Optional[str] = None

class NoteCreate(NoteBase):
    pass

class NoteUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None   # FIXED (was `content`)

class NoteResponse(NoteBase):
    id: int
    owner_id: int
    sentiment: str

    class Config:
        from_attributes = True


# ---------- Users ----------
class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True


# ---------- Token ----------
class Token(BaseModel):
    access_token: str
    token_type: str
