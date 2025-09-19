from . import db

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


class Comment(db.model):
    id = db.Column(db.Integer, primary_key=True)
    user_id= db.Column(db.Integer, db.ForeignKey('user.id', ondelete="CASCADE", nullable=False))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    text=db.Column(db.Text,nullable=False)


