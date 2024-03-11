from flask import Flask, request, jsonify
from models import *
from config import Config
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, unset_jwt_cookies
from flask_cors import CORS

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'veryyysecret'

app = Flask(__name__)
app.config.from_object(Config)
jwt = JWTManager(app)
db.init_app(app)
bcrypt = Bcrypt(app)
with app.app_context():
    db.create_all()

CORS(app, supports_credentials=True)

# Home route
@app.route("/")
def hello():
    return "Hello, World!"

# register route
@app.route("/register", methods = ["POST"])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    name = data.get('name')
    role = data.get('role')

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 409
    
    new_user = User(name=name, email=email, password=password, role=role)

    try: 
        db.session.add(new_user)
        db.session.commit()
        if role == "manager":
            return jsonify({"message": "Manager application submitted"}), 201
        else:
            return jsonify({"message": "User created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error creating user"}), 500
    
@app.route("/login", methods = ["POST"])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user:
        return jsonify({"error": "User not found, Try registering first"}), 404
    
    if not bcrypt.check_password_hash(user.password, password):
        return jsonify({"error": "Incorrect password"}), 401
    
    if user.role == "manager" and not user.verified:
        return jsonify({"error": "Manager application not verified"}), 401

    access_token = create_access_token(identity={
        'id': user.id,
        'role': user.role,
        'verified': user.verified
    })

    return jsonify({"message": "Login successful", "access_token": access_token}), 200


@app.route("/protected")
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    if current_user['role'] != "admin":
        return jsonify({"error": "Verry Protected Route, You don't have auth"}), 401
    return jsonify({"message": "Hi Admin"}), 200


if __name__ == "__main__":
    app.run(debug=True)