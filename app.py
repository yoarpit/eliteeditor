from flask import Flask,render_template,request,redirect,session,flash,url_for
from flask_sqlalchemy import *
from werkzeug.utils import secure_filename

from datetime import datetime
import cv2,os
 

app = Flask(__name__)

app.config['SECRET_KEY'] = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'



app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:ansh@localhost/elite'
db = SQLAlchemy(app)


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'webp', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

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





def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def processImage(filename, operation):
    print(f"the operation is {operation} and filename is {filename}")
    img = cv2.imread(f"uploads/{filename}")
    match operation:
        case "cgray":
            imgProcessed = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            newFilename = f"static/{filename}"
            cv2.imwrite(newFilename, imgProcessed)
            return newFilename
        case "cwebp": 
            newFilename = f"static/{filename.split('.')[0]}.webp"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cjpg": 
            newFilename = f"static/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cpng": 
            newFilename = f"static/{filename.split('.')[0]}.png"
            cv2.imwrite(newFilename, img)
            return newFilename

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
            return redirect("/editor")

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
         session.pop("password",None)
         return redirect("/login")
   




@app.route("/about")
def about():
    return render_template("about.html")





@app.route("/editor",methods=["POST","GET"])
def editor():

 if request.method == "POST": 
        # operation = request.form.get("operation")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "error no selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # new = processImage(filename, operation)

 return render_template("editor.html")

@app.route("/convert", methods=["GET", "POST"])
def con():
    if request.method == "POST": 
        operation = request.form.get("operation")
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return "error"
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return "error no selected file"
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new = processImage(filename, operation)
            flash(f"Your image has been processed and is available <a href='/{new}' target='_blank'>here</a>")
            return render_template("convert.html")

    return render_template("convert.html")



if __name__ == "__main__":
    app.run(debug=True)