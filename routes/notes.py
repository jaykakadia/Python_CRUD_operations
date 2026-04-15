from models import Note, NoteModel, NoteUpdateModel, User
from flask import Blueprint, request, jsonify
from extensions import db
from pydantic import ValidationError
from flask_jwt_extended import current_user, jwt_required, get_jwt_identity
import json

notes_bp = Blueprint("notes", __name__)


@notes_bp.route("/notes", methods=["POST"])
@jwt_required()
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
    
    current_user = json.loads(get_jwt_identity())

    # Add to db
    try:    
        note = Note(title=data.title, content=data.content, user_id=current_user['id'])
        db.session.add(note)
        db.session.commit()
        return {"message": "Created", "id": note.id}
    except Exception as e:
        return jsonify({"message": str(e)}), 500



@notes_bp.route("/notes/<int:id>", methods = ["PUT"])
@jwt_required()
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
        
    current_user = json.loads(get_jwt_identity()) # get user from db
    if note.user_id != current_user['id'] and current_user['role'] != 'admin':
        return jsonify({"message": "Unauthorized"}), 403

    if not data.title or not data.content:
        return {"message": "Title and content are required"}, 400
    
    note.title = data.title
    note.content = data.content
    
    try:    
        db.session.commit()
        return {"message": "Updated", "id": note.id}
    except Exception as e:
        return jsonify({"message": str(e)}), 500
    

@notes_bp.route("/notes/<int:id>", methods = ["PATCH"])
@jwt_required()
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
        
    current_user = json.loads(get_jwt_identity())
    if note.user_id != current_user['id'] and current_user['role'] != 'admin':
        return jsonify({"message": "Unauthorized"}), 403

    if data.title is not None:
        note.title = data.title

    if data.content is not None:
        note.content = data.content
    try:    
        db.session.commit()
        return {"message": "Updated", "id": note.id}
    except Exception as e:
        return jsonify({"message": str(e)}), 400
    
@notes_bp.route("/notes/<int:id>", methods = ["GET"])
@jwt_required()
def get_note(id):
    """
    Function to get a note in the db 
    """
    try:
        note = Note.query.get(id)
        if not note:
            return {"message": "Note not found"}, 404

        current_user = json.loads(get_jwt_identity())
        if note.user_id != current_user['id'] and current_user['role'] != 'admin':
            return jsonify({"message": "Unauthorized"}), 403
        
        return {"id": note.id, "title": note.title, "content": note.content}
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@notes_bp.route("/notes/<int:id>", methods = ["DELETE"])
@jwt_required()
def delete_note(id):
    """
    Function to Delete an note in the db 
    """
    note = Note.query.get_or_404(id)

    current_user = json.loads(get_jwt_identity())
    if note.user_id != current_user['id'] and current_user['role'] != 'admin':
        return jsonify({"message": "Unauthorized"}), 403

    try:
        db.session.delete(note)
        db.session.commit()
        return {"message": "Deleted"}
    except Exception as e:
        return jsonify({"message": str(e)}), 500


@notes_bp.route("/allNotes", methods=["GET"])
@jwt_required()
def get_notes():
    try:
        current_user = json.loads(get_jwt_identity())
        
        if current_user['role'] == 'admin':
            # Admin sees all notes
            notes = Note.query.all()
        else:
            # User sees only their notes
            notes = Note.query.filter_by(user_id=current_user['id']).all()
            
        return jsonify([
            {"id": n.id, "title": n.title, "content": n.content, "user_id": n.user_id, "username": n.author.username if n.author else "Unknown"}
            for n in notes
        ])
    except Exception as e:
        return jsonify({"message": str(e)}), 500

from sqlalchemy import text

@notes_bp.route("/reset-db", methods=["DELETE"])
@jwt_required()
def reset_db():
    current_user = json.loads(get_jwt_identity())

    # Check if user is admin
    if current_user['role'] != 'admin':
        return {"message": "Unauthorized"}, 403

    try:
        # Disable foreign key checks
        db.session.execute(text("SET FOREIGN_KEY_CHECKS = 0"))

        # Truncate tables
        db.session.execute(text("TRUNCATE TABLE note"))
        db.session.execute(text("TRUNCATE TABLE user"))

        # Enable foreign key checks
        db.session.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

        db.session.commit()

        return {"message": "Database reset successful"}

    except Exception as e:
        db.session.rollback()  # important!
        return {"message": str(e)}, 500