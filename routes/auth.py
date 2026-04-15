from flask import Blueprint, request, jsonify
from models import User, UserAuthModel
from extensions import db, bcrypt
from flask_jwt_extended import create_access_token
from pydantic import ValidationError

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = UserAuthModel(**request.json)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    if User.query.filter_by(username=data.username).first():
        return jsonify({"message": "Username already exists"}), 400

    if data.role not in ['user', 'admin']:
        return jsonify({"message": "Invalid role. Must be 'user' or 'admin'"}), 400

    hashed_password = bcrypt.generate_password_hash(data.password, rounds=13).decode('utf-8')
    new_user = User(username=data.username, password_hash=hashed_password, role=data.role)
    
    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"message": "User created successfully", "role": data.role}), 201
    except Exception as e:
        return jsonify({"message": str(e)}), 500

@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = UserAuthModel(**request.json)
    except ValidationError as e:
        return jsonify(e.errors()), 400

    user = User.query.filter_by(username=data.username).first() # get user from db

    if not user or not bcrypt.check_password_hash(user.password_hash, data.password): # check if user exists and password is correct
        return jsonify({"message": "Invalid username or password"}), 401

    import json
    # include id and role in the token's identity as a JSON string to avoid 422 errors
    access_token = create_access_token(identity=json.dumps({'id': user.id, 'role': user.role}))
    
    return jsonify(access_token=access_token, role=user.role), 200
