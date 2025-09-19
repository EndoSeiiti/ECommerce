from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user


app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/api/products', methods=['GET'])
    def get_products():
        products = Product.query.all()
        products_list = []
        for product in products:
            products_list.apend({
                'id': product.id,
                'name': product.name,
                'description': product.description,
                'price': product.price,
                'image_url': product.image_url
            })
            return jsonify(products_list)

@app.route('/api/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'description': product.text,
        'price': product.price,
        'image_url': product.image_url,
        'username': product.user.username,
        'date_created': product.date_created,
        'rating': product.rate,
        'purchases': product.purchases,
        'comments': product.comments
        })


@app.route('/api/user/<int:user_id>',methods=['GET'])
    def get_userdata(user_id):
        user = User.query.get_or_404(user_id)
        user_products=[]
        for product in products:
            user_products.append({
                'id':product.id,
                'name': product.name,
                'price': product.price,
                'image_url':product.image_url
            })
        

        return jsonify({
            'username': user.username,
            'products': user.products,
            'email': user.email

        })

@app.route ('/api/register', methods=['POST'])
def register_user():
    data= request.get_json()

    email= data.get('email')
    username = data.get('username')
    password = data.get('password')

    if not email or not usename or not password:
        return jsonify({'error':'Please fill all fields'}),400
    
    try: 
        hashed_password = generate_password_hash(password)
        new_user = User(
            email = email
            username=username
            password= hashed_password
            
        )
        db.session.add(new_user)
        da.session.commit()
        
        return jsonify({'message': "User successfully registered "}),201

    except Exception as e:
        return jsonify({'error':'This user or email already exists'}), 409

@app.route ('/api/login',methods=['POST'])
def login():
    data=request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        login_user (user)
        return jsonify({
            'message': Login successfull!,
            'user_id': user.id
        }), 200
        else return jsonify({'error': 'User or password incorrect'})