from flask import Flask,request,jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_cors import CORS
from flask_migrate import Migrate
from flask_mail import Mail,Message
from threading import Thread
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:root@localhost/mempage_users"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAIL_SERVER']="smtp.googlemail.com"
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=1
app.config['MAIL_USERNAME']="rajendercherry9@gmail.com"
app.config['MAIL_PASSWORD']="cherry@123"
db = SQLAlchemy(app)
migrate = Migrate(app, db)
CORS(app)
mail = Mail(app)
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    email = db.Column(db.String(64),unique=True)
    number = db.Column(db.String(64),unique=True)
    description = db.Column(db.String(1000))
    country = db.Column(db.String(20))


def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)
def send_mail(subject,sender,recipients,text_body,html_body):
    msg = (subject,sender=sender,recipients=recipients)
    msg.body=text_body
    msg.html=html_body
    Thread(target=send_async_email, args=(app, msg)).start()

@app.route('/user', methods=['POST'])
def user():
    user = User(name=request.json["name"],
                email=request.json["email"],
                number=request.json['country_code']+request.json["number"],
                description=request.json["description"],
                country=request.json['country']                
    db.session.add(user)
    db.session.commit()
    send_mail('Mempage registration','rajendercherry9@gmail.com',['rajendercherry9@gmail.com'],'textbody','<h1>HTML Body<h1>')
    return jsonify({"hai":"how are you"})


