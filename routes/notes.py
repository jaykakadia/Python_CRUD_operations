from models import Note, NoteModel
from flask import Blueprint, request, jsonify
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
    if not data.title or not data.content:
        return {"message": "Title and content are required"}, 400 
    
    # Add to db
    try:    
        note = Note(title=data.title, content=data.content)
        db.session.add(note)
        db.session.commit()
        return {"message": "Created", "id": note.id}
    except Exception as e:
        return jsonify({"message": str(e)}), 500



@notes_bp.route("/notes/<int:id>", methods = ["PUT"])
def update_note(id):
    """
    Function to update a note in the db 
    """

    note = Note.query.get(id)

    try:   # validation check
        data = NoteModel(**request.json)
    except ValidationError as e:
        return jsonify(e.errors()), 400
    
    if not note:
        return {"message": "Note not found"}, 404
    if not data.title or not data.content:
        return {"message": "Title and content are required"}, 400
    
    try:    
        db.session.commit()
        return {"message": "Updated", "id": note.id}
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    

@notes_bp.route("/notes/<int:id>", methods = ["PATCH"])
def updatePartial_note(id):
    """
    Function to Partial update a note in the db 
    """

    note = Note.query.get(id)

    try:   # validation check
        data = NoteUpdateModel(**request.json)
    except ValidationError as e:
        return jsonify(e.errors()), 400
    
    if not note:
        return {"message": "Note not found"}, 404
        
    if data.title is not None:
        note.title = data.title

    if data.content is not None:
        note.content = data.content
    try:    
        db.session.commit()
        return {"message": "Updated", "id": note.id}
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    
@notes_bp.route("/notes/<int:id>", methods = ["GET"])
def get_note(id):
    """
    Function to get a note in the db 
    """
    try:
        note = Note.query.get(id)
        if not note:
            return {"message": "Note not found"}, 404
        
        return {"id": note.id, "title": note.title, "content": note.content}
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@notes_bp.route("/notes/<int:id>", methods = ["DELETE"])
def delete_note(id):
    """
    Function to Delete an note in the db 
    """
    note = Note.query.get_or_404(id)

    try:
        db.session.delete(note)
        db.session.commit()
        return {"message": "Deleted"}
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@notes_bp.route("/allNotes", methods=["GET"])
def get_notes():
    try:
        notes = Note.query.all()
        return jsonify([
            {"id": n.id, "title": n.title, "content": n.content}
            for n in notes
        ])
    except Exception as e:
        return jsonify({"message": str(e)}), 500
