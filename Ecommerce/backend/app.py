from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, current_user



app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173", "supports_credentials": True}})
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ecommerce.db'
app.config['SECRET_KEY'] = 'minhachave' 
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax' 
app.config['SESSION_COOKIE_SECURE'] = False    
db = SQLAlchemy(app)
from models import User

with app.app_context():
    db.create_all()

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route('/api/products', methods=['GET'])
def get_products():
        products = product.query.all()
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

    if not email or not username or not password:
        return jsonify({'error':'Please fill all fields'}),400

    existing_user = User.query.filter_by(username=username).first()
    existing_email = User.query.filter_by(email=email).first()
    
    if existing_user or existing_email:
        return jsonify({'error': 'This user or email already exists'}), 409
    
    try: 
        hashed_password = generate_password_hash(password)
        new_user = User(
            email = email,
            username=username,
            password= hashed_password
            
        )
        db.session.add(new_user)
        db.session.commit()
        
        return jsonify({'message': "User successfully registered "}),201

    except Exception as e:
        print(f"Erro inesperado durante o registro: {e}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

@app.route ('/api/login',methods=['POST'])
def login():
    data=request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        login_user (user,  remember=True)
        return jsonify({
            'message': 'Login successfull!',
            'user_id': user.id
        }), 200
    else:
             return jsonify({'error': 'User or password incorrect'}), 401

@app.route ('/api/products', methods=['POST'])
@login_required
def addproduct():
    data = request.get_json()
    if not all (key in data for key in ['name', 'description', 'price', 'image_url']):
        return jsonify({'error': 'Faltam dados obrigatórios do produto'}), 400

    new_product = Product(
        name= data['name'],
        description = data['description'],
        price = data['price'],
        image_url = data['image_url'],
        user_id=current_user.id
    )

    db.session.add(new_product)
    db.session.commit()

    return jsonify({
        'message':'Product added successfuly!',
        'id': new_product.id
    }),201

@app.route ('/api/products/<int:product_id>', methods=['PUT'])
@login_required

def update_product(product_id):
    product = Product.query.get_or_404(product_id)

    if product.user_id != current_user.id:
        return jsonify({'error': 'You do not have permition to edit this product'})

    data = request.get_json()

    product.name = data.get('name', product.name),
    product.description = data.get('description', product.description),
    product.price = data.get('price', product.price),
    product.image_url = data.get('image_url', product.image_url)

    db.session.commit()

    return jsonify({
        'message':'Product updated!'
    }), 200

@app.route ('/api/products/<int:product_id>',methods=['DELETE'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    if product.user_id != current_user.id:
        return jsonify({'error': 'You do not have permition to edit this product'})

    db.session.delete(product)
    db.session.commit()

    return jsonify ({
        'message': 'Product deleted seccessfuly'
    }), 200

@app.route ('/api/orders', methods=['POST']) 
@login_required

def new_order():
    items_data = request.get_json()
    if not items_data:
        return jsonify({'error': 'Nenhum item foi fornecido'}), 400

    new_order = Order(user_id=current_user.id, total_price=0.0)

    db.session.add(new_order)
    db.session.commit()

    total_price = 0

    for item_data in items_data:
        product_id = item_data.get('product_id')
        quantity = item_data.get('quantity')

        product = Product.query.get_or_404(product_id)

        order_item = OrderItem(
            order_id = new_order.id,
            product_id= product.id,
            quantity = quantity, 
            price = product.price
        )
        db.session.add(order_item)
        total_price  += product.price * quantity

        new_order.total_price=total_price
        db.session.commit()

        return jsonify({
            'message':'Ordered successfuly',
            'order_id': new_order.id
        }), 201    
        
@app.route ('/api/user/<int:user_id>/orders', methods=['GET'])
@login_required
def get_user_orders(user_id):
    if current_user.id != user_id:
        return jsonify({'error': 'Você não tem permissão para ver estes pedidos'})

    user_orders = Order.query.filter_by(user_id=user_id).order_by(Order.date_created.desc()).all()  

    orders_list = []
    
    for order in user_orders:
        order_items_list = []
        
        for item in order.items:
            order_items_list.append({
                'product_id': item.product_id,
                'quantity': item.quantity,
                'price': item.price_at_purchase
            })
            
        orders_list.append({
            'order_id': order.id,
            'date_created': order.date_created,
            'total_price': order.total_price,
            'items': order_items_list
        })
    
    return jsonify(orders_list)   
        

