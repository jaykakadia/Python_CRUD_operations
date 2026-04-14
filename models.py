from extensions import db
from pydantic import BaseModel
from typing import Optional

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(500))


class NoteModel(BaseModel):
    title: str
    content: str



class NoteUpdateModel(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
