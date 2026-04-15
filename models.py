from extensions import db
from pydantic import BaseModel
from typing import Optional

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), default='user') # 'user' or 'admin'
    notes = db.relationship('Note',
                            backref='author', # gives the user who created the note
                            lazy=True, # 👉 Loads data only when needed
                            cascade="all, delete-orphan") # If user is deleted, all their notes are also deleted but not vice versa

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(500))
    user_id = db.Column(db.Integer,
                        db.ForeignKey('user.id'), # Foreign key to link note to its author
                        nullable=False)


# --- Pydantic Schemas ---

class UserAuthModel(BaseModel):
    username: str
    password: str
    role: Optional[str] = "user"

class NoteModel(BaseModel):
    title: str
    content: str

class NoteUpdateModel(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
