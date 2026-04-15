from flask import Flask
from routes.notes import notes_bp
from routes.auth import auth_bp
from extensions import db, bcrypt
from flask_jwt_extended import JWTManager
from datetime import timedelta
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://root:Ja%40160703@localhost:3306/flask_app" 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False # Disable to save resources (if true if will save all the changes to the db in memory which can cause memory leak)

app.config["JWT_SECRET_KEY"] = "super-secret-key-12345"  #jwt secret key through which the JWT verify user
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=2) #time after which JWT expire 
jwt = JWTManager(app) 

db.init_app(app)
bcrypt.init_app(app)

app.register_blueprint(notes_bp)
app.register_blueprint(auth_bp)

if __name__ == "__main__":
    with app.app_context(): # Create application context for DB operations
        # db.drop_all() # Uncomment to drop all tables
        db.create_all() # Create all tables defined in models
    app.run(debug=True, port=5001)