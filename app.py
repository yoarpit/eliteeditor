from flask import Flask,render_template,request,redirect,session
from flask_sqlalchemy import *
from datetime import datetime
import bcrypt
 
app = Flask(__name__)

app.config['SECRET_KEY'] = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'



app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:ansh@localhost/elite'
db = SQLAlchemy(app)



class User(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    email=db.Column(db.String(200),nullable=False)
    password=db.Column(db.String(20),nullable=False)
    date=db.Column(db.String(12),nullable=True)
    
    def __init__(self,email,password,date):
        self.email=email
        self.password=password
        self.date=date

    def check_password(self,password):
        return password,self.password



@app.route("/")
def home():
    return render_template("home.html")




@app.route("/login",methods=['GET','POST'])
def login():
    if (request.method=='POST'):
       email= request.form.get("email")
       password= request.form.get("password")

       entry=User(email=email,password=password,date=datetime.now())
       db.session.add(entry)
       db.session.commit()

       if(not db.session.commit()):
            return redirect("/")

    return render_template("login.html")


@app.route("/signup",methods=["POST","GET"])
def up():
  if (request.method=='POST'):
       email= request.form.get("email")
       password= request.form.get("password")
       user=User.query.filter_by(email=email,password=password).first()


       if user and user.check_password(password):
        session['email']=user.email
        session['password']=user.password
        # session.pop('email',None)
        return render_template('login.html')

  return render_template("signup.html")


@app.route("/loginup")
def loginup():
      if 'email' in session:
         session.pop("email",None)
         return redirect("/login")
   

#    if(drn render_template("index.html")


@app.route("/about")
def about():
    return render_template("about.html")



 
if __name__ == "__main__":
    app.run(debug=True)