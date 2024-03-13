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
ma.init_app(app)
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

@app.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    response = jsonify({'message': 'Logout successful'})
    unset_jwt_cookies(response)
    return response, 200

@app.route('/manager-applications', methods=['GET'])
@jwt_required()
def view_manager_applications():
    current_user = get_jwt_identity()
    if current_user['role'] != "admin":
        return jsonify({"error": "Verry Protected Route, You don't have auth"}), 401
    manager_applications = User.query.filter_by(role='manager', verified=False).all()
    print(manager_applications, type(manager_applications[0]))
    manager_applications = usersschema.dump(manager_applications)
    print(manager_applications, type(manager_applications[0]))
    return jsonify({'manager_applications':manager_applications}), 200


@app.route('/manager-approve/<int:manager_id>', methods=['PUT', 'DELETE'])
@jwt_required()
def manager_approve(manager_id):
    current_user = get_jwt_identity()
    if current_user['role'] != "admin":
        return jsonify({"error": "Verry Protected Route, You don't have auth"}), 401
    manager = User.query.get(manager_id)
    if not manager:
        return jsonify({"error": "Manager not found"}), 404
    if request.method == 'PUT':
        manager.verified = True
        message = "manager Verified"
    elif request.method == 'DELETE':
        db.session.delete(manager)
        message = "manager rejected"
    db.session.commit()
    return jsonify({"message": message}), 200


@app.route('/getuserinfo', methods=['GET'])
@jwt_required()
def getuserinfo():
    this_user = get_jwt_identity()
    user = User.query.get(this_user['id'])
    if not user:
        return jsonify({'message': 'User not found'}), 404
    user_data = userschema.dump(user)
    return jsonify(user_data), 200

# CREATE
@app.route('/category', methods=['POST'])
@jwt_required()
def create_category():
    current_user = get_jwt_identity()
    if current_user['role'] != "admin":
        return jsonify({"error": "Verry Protected Route, You don't have auth"}), 401
    data = request.json
    name = data.get('name')
    existing_category = Category.query.filter_by(name=name).first()
    if existing_category:
        return jsonify({"error": "Category already exists"}), 409
    new_category = Category(name=name)
    try:
        db.session.add(new_category)
        db.session.commit()
        return jsonify({"message": "Category created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error creating category"}), 500

# READ
@app.route('/category/<int:id>', methods=['GET'])
def get_category(id):
    category = Category.query.get(id)
    if not category:
        return jsonify({"error": "Category not found"}), 404
    return jsonify({"category_data":categoryschema.dump(category)}), 200

#UPDATE
@app.route('/category/<int:id>', methods=['PUT'])
@jwt_required()
def update_category(id):
    current_user = get_jwt_identity()
    if current_user['role'] != "admin":
        return jsonify({"error": "Verry Protected Route, You don't have auth"}), 401
    category = Category.query.get(id)
    if not category:
        return jsonify({"error": "Category not found"}), 404
    data = request.json
    name = data.get('name')
    
    category.name = name
    db.session.commit()
    return jsonify({"message": "Category updated successfully"}), 200

#DELETE
@app.route('/category/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_category(id):
    current_user = get_jwt_identity()
    if current_user['role'] != "admin":
        return jsonify({"error": "Verry Protected Route, You don't have auth"}), 401
    category = Category.query.get(id)
    if not category:
        return jsonify({"error": "Category not found"}), 404
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted successfully"}), 200

# Read all categories
@app.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify({"categories":categoriesschema.dump(categories)}), 200

if __name__ == "__main__":
    app.run(debug=True)