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


@notes_bp.route("/notes/<int:id>", methods = ["PUT"])
def update_note(id):
    """
    Function to update a note in the db 
    """
    note = Note.query.get(id)

    if not note:
        return {"message": "Note not found"}, 404

    try:   # validation check
        data = NoteModel(**request.json)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    note.title = data.title
    note.content = data.content
    db.session.commit()

    return {"message": "Updated", "id": note.id}
    
@notes_bp.route("/notes/<int:id>", methods = ["GET"])
def get_note(id):
    """
    Function to get a note in the db 
    """
    note = Note.query.get(id)
    if not note:
        return {"message": "Note not found"}, 404
    
    return {"id": note.id, "title": note.title, "content": note.content}

@notes_bp.route("/notes/<int:id>", methods = ["DELETE"])
def delete_note(id):
    """
    Function to Delete an note in the db 
    """
    note = Note.query.get_or_404(id)

    db.session.delete(note)
    db.session.commit()

    return {"message": "Deleted"}

@notes_bp.route("/allNotes", methods=["GET"])
def get_notes():
    notes = Note.query.all()
    return jsonify([
        {"id": n.id, "title": n.title, "content": n.content}
        for n in notes
    ])
