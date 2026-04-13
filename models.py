from extensions import db
from pydantic import BaseModel

class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    content = db.Column(db.String(500))


class NoteModel(BaseModel):
    title: str
    content: str