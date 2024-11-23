from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import *
from datetime import datetime
#from flask_mail import mail
 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:ansh@localhost/elite'
db = SQLAlchemy(app)



class User(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(200),nullable=False)
    password=db.Column(db.String(20),nullable=False)
    date=db.Column(db.String(12),nullable=True)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/signin")
def sign():
    return render_template("signin.html")


@app.route("/login",methods=['GET','POST'])
def login():
    if (request.method=='POST'):
       email= request.form.get("email")
       password= request.form.get("password")

       entry=User(email=email,password=password,date=datetime.now())
       db.session.add(entry)
       db.session.commit()
      # mail.send_message("new message from blog",sender=email,recipents={params{'gmail=user'}})
       if(db.session.commit()):
           return render_template("index.html")

    return render_template("login.html")


@app.route("/signup")
def up():
    return render_template("signup.html")

@app.route("/drop")
def drop():
    return render_template("dropdown.html")

 
if __name__ == "__main__":
    app.run(debug=True)