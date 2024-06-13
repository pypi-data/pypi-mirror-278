

def get() :
    """List titles in feed."""
    articles="""
##########################################################################################models.py

from ecommerceapp import db
from datetime import datetime

class Product(db.Model):
    product_id=db.Column(db.Integer,primary_key=True)
    product_name=db.Column(db.String(80),nullable=False)
    price=db.Column(db.Float,nullable=False)
    seller_id=db.Column(db.Integer, db.ForeignKey('user.user_id'))
    category_id=db.Column(db.Integer, db.ForeignKey('category.category_id'))
    
class Category(db.Model):
    category_id=db.Column(db.Integer,primary_key=True)
    category_name=db.Column(db.String(80),nullable=False)
    #products=db.relationship("Product", cascade="all, delete-orphan", backref='category')
    
    
class Cart(db.Model):
    cart_id=db.Column(db.Integer,primary_key=True)
    total_amount=db.Column(db.Float,nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.user_id'))
    #cartproducts=db.relationship("CartProduct", cascade="all, delete-orphan", backref='cart')
    
class CartProduct(db.Model):
    cp_id=db.Column(db.Integer,primary_key=True)
    cart_id=db.Column(db.Integer, db.ForeignKey('cart.cart_id'))
    product_id=db.Column(db.Integer, db.ForeignKey('product.product_id'))
    quantity=db.Column(db.Integer)

class Role(db.Model):
    role_id=db.Column(db.Integer,primary_key=True)
    role_name=db.Column(db.String(20),nullable=False)
    #users=db.relationship("User", cascade="all, delete-orphan", backref='role')
    
    
class User(db.Model):
    user_id=db.Column(db.Integer,primary_key=True)
    user_name=db.Column(db.String(20),nullable=False)
    password=db.Column(db.String(150),nullable=False)
    user_role=db.Column(db.Integer, db.ForeignKey('role.role_id'))
    

    
#########################################################################routes.py

from flask import Flask, request, jsonify, make_response, session, app, Response,url_for
from ecommerceapp import app, db
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate #MigrateCommand

from datetime import datetime,timedelta
import os
from sqlalchemy.orm import sessionmaker
    
import json
import jwt
from functools import wraps

from .models import Product,Category,Cart,CartProduct,Role,User
# importing the module
import base64
'''
NOTE:
Use jsonify function to return the outputs and status code

Example:
with output
return jsonify(output),2000

only status code
return '',404


'''


# Use this token_required method for your routes where ever needed.
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        current_user={}
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'Message':'Token is missing'}), 401
        try:
            
            data = jwt.decode(token, 'shit',algorithms=['HS256'])
            #ures = User.query.filter_by(user_id=data['id']).first()
            
            current_user['id']=data['id']
            current_user['role']=data['role']
        except Exception as e:
            print(e)
            return jsonify({'Message': 'Token is invalid'}), 401
        return f(current_user, *args, **kwargs)
    return decorated


    
#Write your code here for the API end point

@app.route('/api/public/login')
def plogin():
    res=[]
    encoded_cred = request.headers['Authorization'].lstrip('Basic').strip()
    print(encoded_cred)
    cred = base64.b64decode(encoded_cred).decode("utf-8")
    print()
    creds = cred.split(':')
    un = creds[0].strip()
    
    data = db.session.query(User, Role).filter(User.user_role == Role.role_id,).filter(User.user_name==un).all()
    
    if data:
        if check_password_hash(data[0][0].password,creds[1].strip()):
            data = jwt.encode(
                payload={'id':data[0][0].user_id,'role':data[0][1].role_name},
                key='shit'
            ).decode('utf-8')
            return {'token':data},200
    
    return '',401




    return ''


@app.route('/api/auth/seller/product/<id>')
@token_required
def sellerproducti(current_user,id):
    res=[]
    if current_user['role']!='SELLER':
        return '403',403
    data = db.session.query(Product, Category).filter(Product.category_id == Category.category_id,).filter(Product.product_id==int(id)).first()
    
    if data:
        dat=data

        if int(dat[0].seller_id) != int(current_user['id']):
            return '',404

        res.append({"category":{"category_id":dat[1].category_id,"category_name":dat[1].category_name},"price":dat[0].price,"product_id":dat[0].product_id,"product_name":dat[0].product_name,"seller_id":dat[0].seller_id})
            
        return json.dumps(res,separators=(',', ':')),200
    else:
        return '404',404


@app.route('/api/auth/seller/product',methods = ['GET'])
@token_required
def sellerproduct(current_user):
    res=[]
    if current_user['role']!='SELLER':
        return '',403
    data = db.session.query(Product, Category).filter(Product.category_id == Category.category_id,).filter(Product.seller_id==current_user['id']).all()
    
    if data:
        for dat in data:
            res.append({"category":{"category_id":dat[1].category_id,"category_name":dat[1].category_name},"price":dat[0].price,"product_id":dat[0].product_id,"product_name":dat[0].product_name,"seller_id":dat[0].seller_id})
            
        return json.dumps(res,separators=(',', ':')),200
    else:
        return '',400

@app.route('/api/auth/seller/product',methods = ['POST'])
@token_required
def sellerproductinsert(current_user):
    if current_user['role']!='SELLER':
        return '',403

    data= request.json
    product_id=data['product_id']
    product_name=data['product_name']
    price=data['price']
    seller_id=current_user['id']
    category_id=data['category_id']

    data = db.session.query(Product).filter(Product.product_id == product_id,Product.seller_id==current_user['id']).first()
    
    if data:
        return '',409

    inp= Product(product_id=product_id,product_name=product_name,price=price,seller_id=seller_id,category_id=category_id)
    db.session.add(inp)   
    db.session.commit()

    return str(product_id),201

@app.route('/api/auth/seller/product',methods = ['PUT'])
@token_required
def sellerproductupdate(current_user):
    if current_user['role']!='SELLER':
        return '',403

    data= request.json
    product_id=data['product_id']
    price=data['price']

    data = db.session.query(Product).filter(Product.product_id == product_id,Product.seller_id==current_user['id']).first()
    
    if data:
        data.price=price
        db.session.add(data)   
        db.session.commit()
        return '',200
    else:
        return '',404

@app.route('/api/auth/seller/product/<id>',methods = ['DELETE'])
@token_required
def sellerproductdelete(current_user,id):
    if current_user['role']!='SELLER':
        return '',403

    data = db.session.query(Product).filter(Product.product_id == id,Product.seller_id==current_user['id']).first()
    
    if data:
        db.session.delete(data)   
        db.session.commit()
        return '',200
    else:
        return '',404


@app.route('/api/public/product/search')
def search():
    res=[]
    key = request.args.get('keyword')

    data = db.session.query(Product, Category).filter(Product.category_id == Category.category_id,).filter(Product.product_name.contains(key)).all()
    
    if data:
        for dat in data:
            res.append({"category":{"category_id":dat[1].category_id,"category_name":dat[1].category_name},"price":dat[0].price,"product_id":dat[0].product_id,"product_name":dat[0].product_name,"seller_id":dat[0].seller_id})
            
        return json.dumps(res,separators=(',', ':')),200
    else:
        return '',400



@app.route('/api/auth/consumer/cart',methods = ['GET'])
@token_required
def consumercart(current_user):
    res=[]
    if current_user['role']!='CONSUMER':
        return '',403
    data = db.session.query(Cart,CartProduct,Product,Category).filter(Cart.cart_id==CartProduct.cart_id,
        CartProduct.product_id==Product.product_id,
        Product.category_id==Category.category_id,Cart.user_id==current_user['id']).all()

    if data:
        for dat in data:
            res.append({"cart_id":dat[0].cart_id,
            "cartproducts":
                {"cp_id":dat[1].cp_id,"product":{
                    "category":
                        {"category_id":dat[3].category_id,"category_name":dat[3].category_name},
                    "price":dat[2].price,
                    "product_id":dat[2].product_id,
                    "product_name":dat[2].product_name}},
            "total_amount":dat[0].total_amount})
            
        return json.dumps(res,separators=(',', ':')),200
    else:
        return '',400

@app.route('/api/auth/consumer/cart',methods = ['POST'])
@token_required
def consumercartadd(current_user):
    res=[]
    if current_user['role']!='CONSUMER':
        return '',403

    data = request.json
    product_id=data['product_id']
    quantity=data['quantity']

    data = db.session.query(Cart).filter(Cart.user_id==current_user['id']).first()

    if data:
        cpdata=db.session.query(CartProduct).filter(CartProduct.cart_id==data.cart_id,CartProduct.product_id==product_id,CartProduct.quantity==quantity).first()
        if cpdata:
            return '',409
        ins = CartProduct(cart_id=data.cart_id,product_id=product_id,quantity=quantity)
        db.session.add(ins)   
        db.session.commit()

        pdata = db.session.query(Product).filter(Product.product_id==product_id).first()
        data.total_amount+=int(quantity)*pdata.price
        db.session.add(data)   
        db.session.commit()
        return str(data.total_amount),200
    

@app.route('/api/auth/consumer/cart',methods = ['PUT'])
@token_required
def consumercartupdate(current_user):
    res=[]
    if current_user['role']!='CONSUMER':
        return '',403

    data = request.json
    product_id=data['product_id']
    quantity=data['quantity']

    data = db.session.query(Cart).filter(Cart.user_id==current_user['id']).first()

    if data:
        cpdata=db.session.query(CartProduct).filter(CartProduct.cart_id==data.cart_id,CartProduct.product_id==product_id).first()
        if cpdata:
            pdata = db.session.query(Product).filter(Product.product_id==product_id).first()
            data.total_amount-=int(cpdata.quantity)*pdata.price
            cpdata.quantity=quantity
            data.total_amount+=int(quantity)*pdata.price
            db.session.add(cpdata)   
            db.session.add(data)
            db.session.commit()
            
        else:
            return '',404
        
        return str(data.total_amount),200

@app.route('/api/auth/consumer/cart',methods = ['DELETE'])
@token_required
def consumercartdelete(current_user):
    if current_user['role']!='CONSUMER':
        return '',403

    data = request.json
    product_id=data['product_id']

    data = db.session.query(Cart).filter(Cart.user_id==current_user['id']).first()

    if data:
        cpdata=db.session.query(CartProduct).filter(CartProduct.cart_id==data.cart_id,CartProduct.product_id==product_id).first()
        if cpdata:
            pdata = db.session.query(Product).filter(Product.product_id==product_id).first()
            data.total_amount-=int(cpdata.quantity)*pdata.price
            db.session.delete(cpdata)   
            db.session.add(data)
            db.session.commit()
            return str(data.total_amount),200
        else:
            return '',404


#################################################init.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import BaseConfig
from flask_migrate import Migrate

app = Flask(__name__)
app.debug=True
app.config.from_object(BaseConfig)
db = SQLAlchemy(app)
migrate = Migrate(app, db)



from . import routes, models    


#do not delete these below methods
@app.cli.command()
def erasedata():
    db.drop_all()
    db.session.commit()
    db.create_all()
@app.cli.command()
def seeddata():
    from . import seed

    #########################################################################seed.py
from werkzeug.security import generate_password_hash
from . import db
from .models import Product, Role, Cart, CartProduct, Category,User

db.drop_all()
db.session.commit()
try:
    db.drop_all()
    db.create_all()
    c1=Category(category_name='Fashion')
    db.session.add(c1)
    db.session.commit()

    c2=Category(category_name='Electronics')
    db.session.add(c2)
    db.session.commit()

    c3=Category(category_name='Books')
    db.session.add(c3)
    db.session.commit()

    c4=Category(category_name='Groceries')
    db.session.add(c4)
    db.session.commit()

    c5=Category(category_name='Medicines')
    db.session.add(c5)
    db.session.commit()


    r1=Role(role_name='CONSUMER')
    db.session.add(r1)
    db.session.commit()

    r2=Role(role_name='SELLER')
    db.session.add(r2)
    db.session.commit()

    password=generate_password_hash("pass_word",method='pbkdf2:sha256',salt_length=8)
    u1=User(user_name='jack',password=password,user_role=1)
    db.session.add(u1)
    db.session.commit()

    u2=User(user_name='bob',password=password,user_role=1)
    db.session.add(u2)
    db.session.commit()

    u3=User(user_name='apple',password=password,user_role=2)
    db.session.add(u3)
    db.session.commit()

    u4=User(user_name='glaxo',password=password,user_role=2)
    db.session.add(u4)
    db.session.commit()

    cart1=Cart(total_amount=20, user_id=1)
    db.session.add(cart1)
    db.session.commit()

    cart2=Cart(total_amount=0, user_id=2)
    db.session.add(cart2)
    db.session.commit()

    p1=Product(price=29190,product_name='ipad',category_id=2,seller_id=3)
    db.session.add(p1)
    db.session.commit()
    p2=Product(price=10,product_name='crocin',category_id=5,seller_id=4)
    db.session.add(p2)
    db.session.commit()

    cp1=CartProduct(cart_id=1,product_id=2,quantity=2)
    db.session.add(cp1)
    db.session.commit()
    print('database successfully initialized')
except Exception:
    db.session.rollback()
    print('error in adding data to db')


"""
    print(articles)
    #return articles


def getjwt() :
    """List titles in feed."""
    articles="""


from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
import json
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity,JWTManager
from datetime import datetime, timedelta
from functools import wraps


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.sqlite3'
app.config['SECRET_KEY'] = "random string"
app.config["JWT_SECRET_KEY"] = "super-secret" 

jwt = JWTManager(app)

db = SQLAlchemy(app)


class userModel(db.Model):
   
    id = db.Column(db.Integer, primary_key = True)
    userid = db.Column(db.Integer)
    name = db.Column(db.String(100))
    password = db.Column(db.String(100))
    phone = db.Column(db.Integer)

    def __init__(self, userid,name,password,phone):
        self.userid=userid
        self.name=name
        self.password=password
        self.phone=phone

class complaintModel(db.Model):

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100))
    message = db.Column(db.String(500))
    date = db.Column(db.Date,default=datetime.now )
    status = db.Column(db.Boolean) 
    userid = db.Column(db.Integer, db.ForeignKey(userModel.id))

    def __init__(self, title,message,date,status,userid):
        self.title = title
        self.message = message
        self.date = date
        self.status = status
        self.userid=userid

def userrequired(f):
    @wraps(f)
    def inner(*args, **kwargs):
        current_user = get_jwt_identity()
        if current_user['role'] == "user":
            print('heree')
            return f(*args, **kwargs)
        else:
            return {'message':'user not authorised'},403
        
    return inner


@app.route('/login',methods=['POST'])
def login():

    userid = request.json.get("userid", None)
    password = request.json.get("password", None)
    

    rcd=userModel.query.filter_by(userid=userid,password=password).first()
    if rcd:
        token = create_access_token(identity={
            'public_id': rcd.id,
            'role': 'user'},expires_delta =  timedelta(days=30))
        return {'token':token}
    else:
        return {'msg':'user not found'},404

@app.route('/uhome')
@jwt_required
@userrequired
def uhome():
    current_user = get_jwt_identity()
    stud=complaintModel.query\
            .filter_by(userid = current_user['public_id'])\
            .all()

    data=[]
    for i in stud:
        data.append({k: v for k, v in i.__dict__.items() if not str(k).startswith("_")})

    return {'result':data}


@app.route('/create', methods = [ 'POST'])
@jwt_required
@userrequired
def create():
    data=json.loads(request.data )
    current_user_id = get_jwt_identity()

    datetime_str = '25/08/1997'
    datetime_object = datetime.strptime(datetime_str, '%d/%m/%Y')

    complaint = complaintModel(title = data['title'],message = data['message'],date=datetime_object,status = True,userid =current_user_id['public_id'])


    db.session.add(complaint)

    db.session.commit()

    db.session.refresh(complaint)

    data={k: v for k, v in complaint.__dict__.items() if not str(k).startswith("_")}

    return jsonify(data)
 
@app.route('/update/<int:id>', methods = [ 'PUT'])
@jwt_required
@userrequired
def update(id):
    data=json.loads(request.data )

    complaint = complaintModel.query.get(id)

    if complaint:
        complaint.title = data['title']
        complaint.message = data['message']
        complaint.status = data['status']

        db.session.commit()

        db.session.refresh(complaint)

        data={k: v for k, v in complaint.__dict__.items() if not str(k).startswith("_")}
        return jsonify(data) 
    else:

        data={'message':'item not found'}

        return jsonify(data),404         


@app.route('/get/<int:id>', methods=['GET'])
@jwt_required
@userrequired
def getone(id):

    complaint = complaintModel.query.get(id)

    if complaint:
        data={k: v for k, v in complaint.__dict__.items() if not str(k).startswith("_")}
        # sub = Subj.query.get(student.Subj)
        # data['sub']=sub.name
        return jsonify(data)

    else:
        return jsonify({'message':'item not found'}),404

@app.route('/delete/<int:id>', methods=['DELETE'])
@jwt_required
@userrequired
def deleteone(id):
    complaint = complaintModel.query.get(id)

    if complaint:
        data={k: v for k, v in complaint.__dict__.items() if not str(k).startswith("_")}

        db.session.delete(complaint)
        db.session.commit()

        return jsonify(data)
    else:
        return jsonify({'message':'item not found'}),404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True)

    """

    print(articles)
    #return articles


def latest():
    articles="""
from flask import Flask, request, jsonify,Blueprint
from flask_sqlalchemy import SQLAlchemy
import json
from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity,JWTManager
from datetime import datetime, timedelta
from functools import wraps
import sqlite3
import sqlalchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///artdb.sqlite3'
app.config['SECRET_KEY'] = "random string"
app.config["JWT_SECRET_KEY"] = "super-secret" 
app.config['JSON_SORT_KEYS'] = False
app.json.sort_keys = False

jwt = JWTManager(app)

db = SQLAlchemy(app)

class Role(db.Model):
   
    id = db.Column(db.Integer, primary_key = True)
    rolename = db.Column(db.String(100),unique=True)
    users = db.Column(db.String(100))
    #date = db.Column(db.Date,default=datetime.now )

class User(db.Model):
   
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(100))
    email = db.Column(db.String(100))
    password = db.Column(db.String(100))
    role_id = db.Column(db.Integer, db.ForeignKey(Role.id))
    arts = db.Column(db.String(100))


class Art(db.Model):
   
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100),unique=True)
    description = db.Column(db.String(100))
    artist = db.Column(db.String(100))
    medium = db.Column(db.String(100))
    price = db.Column(db.Float)
    isAvailable = db.Column(db.Boolean)
    dimensions = db.Column(db.String(100))
    imageLink = db.Column(db.String(100))
    owner_id = db.Column(db.Integer, db.ForeignKey(User.id))

# bp = Blueprint('main', __name__)

# @bp.route('/', methods=('GET', 'POST'))
# def index():
#     return "hello world"

# app.register_blueprint(bp)


@app.route('/user/login',methods=['POST'])
def login():
    data=request.get_json(force=True)
    email=data['email']
    password=data['password']

    rcd=User.query.filter_by(email=email).first()

    if rcd:

        if rcd.password != password:
            return jsonify({'msg':'incorrect password'}),400

        role = Role.query.filter_by(id=rcd.role_id).first()

        token = create_access_token(identity={
            'id': rcd.id,
            'role': role.rolename })#,expires_delta =  timedelta(days=30))

        return jsonify({"username":rcd.username,'token':token}),201

    else:

        return jsonify({'msg':'user not registered'}),400

@app.route('/artwork/list',methods=['GET'])
@jwt_required()
def getart():
    current_user = get_jwt_identity()
    artist = request.args.get('artist')

    if not artist:
        return jsonify({"msg":"artist name need to filter"}),400

    arts = db.session.query(Art).filter(Art.artist.contains(artist.strip())).all()

    res = []
    for i in arts:
        data = {}
        data['id'] = i.id
        data['title'] = i.title
        data['description'] = i.description
        data['artist'] = i.artist
        data['medium'] = i.medium
        data['price'] = i.price
        data['isAvailable'] = i.isAvailable
        data['dimensions'] = i.dimensions
        data['imageLink'] = i.imageLink
        data['owner_id'] = i.owner_id
        res.append(data)
    
    return jsonify(res),200 #json.dumps(res,separators=(',', ':'))

@app.route('/artwork/add',methods=['POST'])
@jwt_required()
def addart():
    current_user = get_jwt_identity()
    
    if current_user['role']!="Owner":
        return jsonify({"msg":"you don't have permission to perform this operation"}),403
    
    data=request.get_json(force=True)
    title = data['title']
    description = data['description']
    artist = data['artist']
    medium = data['medium']
    price = data['price']
    isAvailable = data['isAvailable']
    dimensions = data['dimensions']
    imageLink = data['imageLink']
    owner_id = current_user["id"]

    try:
        data = Art(title=title,description=description,artist=artist,medium=medium,price=price,isAvailable=isAvailable,dimensions=dimensions,imageLink=imageLink,owner_id=owner_id)
        db.session.add(data)
        db.session.commit()
        db.session.refresh(data)
    except sqlalchemy.exc.IntegrityError:
        return jsonify({"msg":"art title need to be unique"}),400

    

    res = {}
    res['id'] = data.id
    res['title'] = data.title
    res['description'] = data.description
    res['artist'] = data.artist
    res['medium'] = data.medium
    res['price'] = data.price
    res['isAvailable'] = data.isAvailable
    res['dimensions'] = data.dimensions
    res['imageLink'] = data.imageLink
    res['owner_id'] = data.owner_id
    
    return jsonify(res),200 #json.dumps(res,separators=(',', ':'))

@app.route('/artwork/update/<int:id>',methods=['PATCH'])
@jwt_required()
def updateart(id):
    current_user = get_jwt_identity()
    
    if current_user['role']!="Owner":
        return jsonify({"msg":"you don't have permission to perform this operation"}),403
    
    data=request.get_json(force=True)
    isAvailable = data['isAvailable']

    try:
        data = db.session.query(Art).filter(Art.id==id).first()
        
        if not data:
            return jsonify({"msg":"art object not found"}),404
        
        if data.owner_id != current_user['id']:
            return jsonify({"msg":"you don't have permission to perform this operation"}),403

        data.isAvailable = isAvailable
        db.session.commit()
        db.session.refresh(data)

    except sqlalchemy.exc.IntegrityError:
        return jsonify({"msg":"art title need to be unique"}),400

    

    res = {}
    res['id'] = data.id
    res['title'] = data.title
    res['description'] = data.description
    res['artist'] = data.artist
    res['medium'] = data.medium
    res['price'] = data.price
    res['isAvailable'] = data.isAvailable
    res['dimensions'] = data.dimensions
    res['imageLink'] = data.imageLink
    res['owner_id'] = data.owner_id
    
    return jsonify(res),200 #json.dumps(res,separators=(',', ':'))

@app.route('/artwork/delete/<int:id>',methods=['DELETE'])
@jwt_required()
def deleteart(id):
    current_user = get_jwt_identity()
    
    if current_user['role']!="Owner":
        return jsonify({"msg":"you don't have permission to perform this operation"}),403

    try:
        data = db.session.query(Art).filter(Art.id==id).first()
        
        if not data:
            return jsonify({"msg":"art object not found"}),404

        if data.owner_id != current_user['id']:
            return jsonify({"msg":"you don't have permission to perform this operation"}),403
        
        db.session.delete(data)
        db.session.commit()

    except sqlalchemy.exc.IntegrityError:
        return jsonify({"msg":"art title need to be unique"}),400
    
    return jsonify(''),204 #json.dumps(res,separators=(',', ':'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug = True)



#{k: v for k, v in i.__dict__.items() if not str(k).startswith("_")}


# from flask_jwt_extended import create_access_token,jwt_required,get_jwt_identity,JWTManager
# from datetime import datetime, timedelta
# from werkzeug.security import check_password_hash, generate_password_hash

# datetime_object = datetime.strptime('25/08/1997', '%d/%m/%Y')


# db.session.refresh(complaint)

# app.config['JWT_TOKEN_LOCATION'] = "headers" #["headers", "cookies", "query_string","json"]
# app.config['JWT_HEADER_NAME'] = "Authorization"
# app.config['JWT_HEADER_TYPE'] = "Bearer"
# app.config['JWT_QUERY_STRING_NAME'] = "jwt"
# app.config['JWT_QUERY_STRING_VALUE_PREFIX'] = "Bearer "
# app.config['JWT_JSON_KEY'] = "access_token"


"""
    print(articles)
    #return articles