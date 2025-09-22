from . import db
from sqlalchemy.sql import func

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    products = db.relationship('Product', backref='user', passive_deletes=True)
    

    

class Product(db.model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    text = db.Column(db.Text, nullable=False )
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE"),nullable=False)
    price = db.Column(db.Float,nullable=False)
    rating = db.Column(db.Float)
    purchases = db.Column(db.Integer)
    comments = db.relationship('Comment', backref='product', passive_deletes=True)
    image_url = db.Column(db.String, nullable=False)

class Order(db.model):
    id = db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id',ondelete="CASCADE",nullable=False))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    status= db.Column(db.Text)
    total_price = db.Column(db.Float)
    itens = db.relationship('OrderItem', backref ='order', passive_deletes=True)

class OrderItems(db.model):
    id = db.Column(db.Integer, primary_key = True)
    order_id = db.Column(db.Integer,db.ForeignKey('order.id', ondelete='CASCADE', nullable=False))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id',ondelete='CASCADE', nullable=False))
    quantity = db.Column(db.Integer, nullable=False) 
    price = db.Column(db.Float, nullable=False)
    

class Comment(db.model):
    id = db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE", nullable=False))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    text=db.Column(db.Text,nullable=False)


