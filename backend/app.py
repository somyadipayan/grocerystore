from flask import Flask, request, jsonify
from models import *
from config import Config
from flask_jwt_extended import JWTManager
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, unset_jwt_cookies
from flask_cors import CORS
import workers, task
from flask_mail import Mail
from mailer import send_email

app = Flask(__name__)
app.config.from_object(Config)
mail = Mail(app)
celery = workers.celery
celery.conf.update(
    broker_url= 'redis://localhost:6379/0',
    result_backend = 'redis://localhost:6379/1'
)
celery.Task = workers.ContextTask
app.app_context().push()
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
    task.add_together.delay(5,3)
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

    user.last_login = datetime.now()

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

# API to create a Product in a Category (can be done by both admin and verified managers)
@app.route('/category/<int:category_id>/add-product', methods=['POST'])
@jwt_required()
def add_product_to_category(category_id):
    try:
        this_user = get_jwt_identity()
        if not this_user['verified']:
            return jsonify({'error': 'Page Restricted!'}), 401

        data = request.json
        print(data)
        product_name = data.get('name')
        product_unit = data.get('unit')
        product_rateperunit = data.get('rateperunit')
        product_quantity = data.get('quantity')

        if not product_name or not product_unit or not product_rateperunit or not product_quantity:
            return jsonify({'message': 'Missing required fields (name, unit, rateperunit, quantity)'}), 400

        new_product = Product(
            name=product_name,
            unit=product_unit,
            rateperunit=product_rateperunit,
            quantity=product_quantity,
            category_id=category_id,
            creator_id=this_user['id']
        )

        db.session.add(new_product)
        db.session.commit()
        task.add_together.delay(new_product)

        return jsonify({'message': 'Product added to category successfully'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

# GET ALL PRODUCTS
@app.route('/products', methods=['GET'])
def view_all_products():
    try:
        all_products = Product.query.all()
        if not all_products:    
            return jsonify({'message': 'No products found.'}), 404
        products_data = productsschema.dump(all_products)
        return jsonify({'products': products_data}), 200
    except Exception as e:
        print(f"Error occurred while fetching products: {str(e)}")
        return jsonify({'message': 'Oops, Something went wrong!'}), 500


@app.route('/products/my-products', methods=['GET'])
@jwt_required()
def view_user_products():
    try:
        this_user= get_jwt_identity()
        if not this_user['verified']:
            return jsonify({'error': 'Page Restricted!'}), 401

        this_user_id = this_user['id']
        user_products = Product.query.filter_by(creator_id=this_user_id).all()
        if not user_products:
            return jsonify({'message': 'You haven\'t added any products'}), 404

        products_data = productsschema.dump(user_products)
        return jsonify({'user_products': products_data}), 200

    except Exception as e:
        print(f"Error occurred while fetching user products: {str(e)}")
        return jsonify({'message': 'Oops, Something went wrong!'}), 500


@app.route('/product/<int:product_id>', methods=['GET'])
def view_product(product_id):
    try:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'message': 'Product not found'}), 404   
        product_data = productschema.dump(product)
        category = Category.query.get(product.category_id)
        return jsonify({'product': product_data, "category_name": category.name}), 200
    except Exception as e:
        print(f"Error occurred while fetching product details: {str(e)}")
        return jsonify({'message': 'Oops, Something went wrong!'}), 500


@app.route('/product/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    try:
        this_user = get_jwt_identity()
        if not this_user['verified']:
            return jsonify({'error': 'Page Restricted!'}), 401

        product = Product.query.get(product_id)
        if not product:
            return jsonify({'message': 'Product not found'}), 404

        data = request.json
        product.name = data.get('name', product.name)
        product.unit = data.get('unit', product.unit)
        product.rateperunit = data.get('rateperunit', product.rateperunit)
        product.quantity = data.get('quantity', product.quantity)

        db.session.commit()

        return jsonify({'message': 'Product updated successfully'}), 200

    except Exception as e:
        print(f"Error occurred while updating product: {str(e)}")
        return jsonify({'message': 'Oops, Something went wrong!'}), 500
    

@app.route('/category/<int:category_id>/products', methods=['GET'])
def view_products_by_category(category_id):
    try:
        products = Product.query.filter_by(category_id=category_id).all()
        if not products:
            return jsonify({'message': 'No products found in this category'}), 404
        products_data = productsschema.dump(products)
        return jsonify({'products': products_data}), 200
    except Exception as e:
        print(f"Error occurred while fetching products: {str(e)}")
        return jsonify({'message': 'Oops, Something went wrong!'}), 500


# ADDING A PRODUCT TO CART
@app.route('/cart/<int:product_id>', methods=['POST'])
@jwt_required()
def addtocart(product_id):
    try:
        current_user = get_jwt_identity()
        product = Product.query.get(product_id)
        
        if not product:
            return jsonify({'message': 'Product not found'}), 404
        
        user_cart = ShoppingCart.query.filter_by(user_id=current_user['id']).first()

        if not user_cart:
            new_cart = ShoppingCart(user_id=current_user['id'])
            db.session.add(new_cart)
            db.session.commit()

        quantity = request.json.get('quantity', 1)
        if quantity < 1:
            return jsonify({'message': 'Quantity must be greater than 0'}), 400
        if quantity > product.quantity:
            return jsonify({'message': 'Quantity exceeds available stock'}), 400
        product_in_cart = CartItem.query.filter_by(cart_id=user_cart.id, product_id=product_id).first()
        print('product_in_cart', product_in_cart)
        if product_in_cart:
            product_in_cart.quantity += quantity
        else:
            print(user_cart.id)
            new_cart_entry = CartItem(cart_id=user_cart.id, product_id=product_id, quantity=quantity)
            print(new_cart_entry)
            db.session.add(new_cart_entry)
        db.session.commit()
        return jsonify({'message': 'Product added to cart successfully'}), 201
    
    except Exception as e:
        print(f"Error occurred while adding product to cart: {str(e)}")
        return jsonify({'message': 'Oops, Something went wrong!'}), 500


@app.route('/cart', methods=['GET'])
@jwt_required()
def viewcart():
    try:
        current_user = get_jwt_identity()
        user = User.query.get(current_user["id"])
        user_cart = ShoppingCart.query.filter_by(user_id=current_user['id']).first()
        if not user_cart:
            return jsonify({'message': 'Cart is empty'}), 404
        cart_items = CartItem.query.filter_by(cart_id=user_cart.id).all()
        if not cart_items:
            return jsonify({'message': 'Cart is empty'}), 404
        cart_data = []
        for cart_item in cart_items:
            product = Product.query.get(cart_item.product_id)
            cart_data.append({
                'product_id': product.id,
                'product_name': product.name,
                'quantity': cart_item.quantity,
                'unit': product.unit,
                'rateperunit': product.rateperunit,
                'total_price': cart_item.quantity * product.rateperunit
            })
        return jsonify({'user': user.name,'cart': cart_data}), 200
    except Exception as e:
        print(f"Error occurred while fetching cart: {str(e)}")
        return jsonify({'message': 'Oops, Something went wrong!'}), 500

@app.route('/order', methods=['POST'])
@jwt_required()
def create_order():
    try:
        current_user = get_jwt_identity()
        user_cart = ShoppingCart.query.filter_by(user_id = current_user['id']).first()

        if not user_cart or not user_cart.items:
            return "Shopping cart is empty"

        total_amount = 0
        order_items = []
        print(user_cart.items)
        for cart_item in user_cart.items:
            print(cart_item)
            product = cart_item.product
            if product.quantity < cart_item.quantity:
                return jsonify({'message': 'Quantity exceeds available stock'}), 400 
            total_amount += cart_item.quantity * product.rateperunit
            order_item = OrderItem(product_id=product.id, quantity=cart_item.quantity)
            order_items.append(order_item)
            product.quantity -= cart_item.quantity
        new_order = Order(user_id = current_user['id'],
                          total_amount = total_amount,
                          order_date = datetime.now())
        new_order.items = order_items
        db.session.add(new_order)
        db.session.delete(user_cart)
        db.session.commit()
        return jsonify({'message': 'Order created successfully'}), 201
    
    except Exception as e:
        print(f"Error occurred while creating order: {str(e)}")
        return jsonify({'message': 'Oops, Something went wrong!'}), 500

if __name__ == "__main__":
    app.run(debug=True)