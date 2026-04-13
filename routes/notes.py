from flask import Blueprint, request, jsonify
from models import Note, NoteModel
from extensions import db
from pydantic import ValidationError

notes_bp = Blueprint("notes", __name__)


@notes_bp.route("/notes", methods=["POST"])
def create_note():
    """
    Function create an note in the db 
    """
    try:   # validation check
        data = NoteModel(**request.json)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    # Add to db
    note = Note(title=data.title, content=data.content)
    db.session.add(note)
    db.session.commit()

    return {"message": "Created", "id": note.id}
