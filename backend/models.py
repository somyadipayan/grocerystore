from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, Text, Boolean, DateTime, ForeignKey
from datetime import datetime
from flask_bcrypt import Bcrypt
from flask_marshmallow import Marshmallow
from sqlalchemy.orm import relationship

db = SQLAlchemy()
bcrypt = Bcrypt()
ma = Marshmallow()

class User(db.Model):
    __tablename__ = "user"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(Text, nullable=False)
    email = Column(Text, nullable=False, unique=True)
    password = Column(Text, nullable=False)
    role = Column(Text, nullable=False) # admin or manager or user
    verified = Column(Boolean, default=False, nullable=False)
    last_logged_in = Column(DateTime, default=datetime.now, nullable=False)

    def __init__(self, name, email, password, role, last_logged_in = datetime.now()):
        self.name = name
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.role = role
        self.last_logged_in = last_logged_in

class Category(db.Model):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    products = relationship('Product', back_populates='category', cascade='all, delete-orphan')
    
    def __init__(self, name):
        self.name = name
    
        
class Product(db.Model):
    __tablename__ = 'product'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    unit = Column(Text, nullable=False)
    rateperunit = Column(Integer, nullable=False)
    quantity = Column(Integer, nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'), nullable=False)
    category = relationship('Category', back_populates='products')
    creator_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    creator = relationship('User', backref='products')
    carts = relationship('CartItem', back_populates='product')
    orders = relationship('OrderItem', back_populates='product')


    def __init__(self, name, unit, rateperunit, quantity, category_id, creator_id):
        self.name = name
        self.unit = unit
        self.rateperunit = rateperunit
        self.quantity = quantity
        self.category_id = category_id
        self.creator_id = creator_id

class ShoppingCart(db.Model):
    __tablename__ = 'shopping_cart'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', backref='shopping_cart')
    items = relationship('CartItem', back_populates='cart', cascade='all, delete-orphan')
    

class CartItem(db.Model):
    __tablename__ = 'cart_item'

    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    product = relationship('Product', back_populates='carts')
    cart_id = Column(Integer, ForeignKey('shopping_cart.id'), nullable=False)
    cart = relationship('ShoppingCart', back_populates='items')
    quantity = Column(Integer, nullable=False)


class Order(db.Model):
    __tablename__ = 'order'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    user = relationship('User', backref='orders')
    items = relationship('OrderItem', back_populates='order', cascade='all, delete-orphan')
    total_amount = Column(Integer, nullable=False)
    order_date = Column(DateTime, default=datetime.now, nullable=False)

class OrderItem(db.Model):
    __tablename__ = 'order_item'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    product = relationship('Product', back_populates='orders')
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    order = relationship('Order', back_populates='items')
    quantity = Column(Integer, nullable=False)

class UserSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "email", "role", "verified")


userschema = UserSchema()
usersschema = UserSchema(many = True)

class CategorySchema(ma.Schema):
    class Meta:
        fields = ('id', 'name')

categoryschema = CategorySchema()
categoriesschema = CategorySchema(many=True)

class ProductSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'unit', 'rateperunit', 'quantity', 'category_id', 'creator_id')

productschema = ProductSchema()
productsschema = ProductSchema(many=True)