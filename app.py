from flask import Flask,render_template,request,redirect,session,flash,url_for,Response,jsonify,send_file, send_from_directory
from flask_sqlalchemy import *
from werkzeug.utils import secure_filename
from datetime import datetime
from deepface import DeepFace
import cv2,os
from authlib.integrations.flask_client import *
import tensorflow as tf 
from PIL import Image
import io





app = Flask(__name__)

app.config['SECRET_KEY'] = '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

app.config['SERVER_NAME'] = 'localhost:5000'


app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:ansh@localhost/elite'
db = SQLAlchemy(app)





UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'png', 'webp', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



# Directories to store images
# UPLOAD_FOLDER = 'static/uploads'
EDITED_FOLDER = 'static/edited'

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(EDITED_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['EDITED_FOLDER'] = EDITED_FOLDER


face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
oauth = OAuth(app)


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
            newFilename = f"static/edited/{filename}"
            cv2.imwrite(newFilename, imgProcessed)
            return newFilename
        case "cwebp": 
            newFilename = f"static/edited/{filename.split('.')[0]}.webp"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cjpg": 
            newFilename = f"static/edited/{filename.split('.')[0]}.jpg"
            cv2.imwrite(newFilename, img)
            return newFilename
        case "cpng": 
            newFilename = f"static/edited/{filename.split('.')[0]}.png"
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





@app.route("/dashboard")
def dash():
    #   if 'email' not in session:
        # flash('Please log in to access the dashboard.', 'warning')
        # return redirect(url_for('login'))
      user = User.query.get(session['email'])
      return render_template('dashboard.html', user=user)


         
   


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



@app.route("/reconigition")
def reco():
    

      
    return render_template("reco.html")






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








@app.route('/google/')
def google():

	# Google Oauth Config
	# Get client_id and client_secret from environment variables
	# For developement purpose you can directly put it 
	# here inside double quotes
	GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
	GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
	
	CONF_URL = 'https://accounts.google.com/.well-known/openid-configuration'
	oauth.register(
		name='google',
		client_id=GOOGLE_CLIENT_ID,
		client_secret=GOOGLE_CLIENT_SECRET,
		server_metadata_url=CONF_URL,
		client_kwargs={
			'scope': 'openid email profile'
		}
	)
	
	# Redirect to google_auth function
	redirect_uri = url_for('google_auth', _external=True)
	return oauth.google.authorize_redirect(redirect_uri)

@app.route('/google/auth/')
def google_auth():
	token = oauth.google.authorize_access_token()
	user = oauth.google.parse_id_token(token)
	print(" Google User ", user)
	return redirect('/')




@app.route('/facebook/')
def facebook():
   
    # Facebook Oauth Config
    FACEBOOK_CLIENT_ID = os.environ.get('FACEBOOK_CLIENT_ID')
    FACEBOOK_CLIENT_SECRET = os.environ.get('FACEBOOK_CLIENT_SECRET')
    oauth.register(
        name='facebook',
        client_id=FACEBOOK_CLIENT_ID,
        client_secret=FACEBOOK_CLIENT_SECRET,
        access_token_url='https://graph.facebook.com/oauth/access_token',
        access_token_params=None,
        authorize_url='https://www.facebook.com/dialog/oauth',
        authorize_params=None,
        api_base_url='https://graph.facebook.com/',
        client_kwargs={'scope': 'email'},
    )
    redirect_uri = url_for('facebook_auth', _external=True)
    return oauth.facebook.authorize_redirect(redirect_uri)
 
@app.route('/facebook/auth/')
def facebook_auth():
    token = oauth.facebook.authorize_access_token()
    resp = oauth.facebook.get( 'https://graph.facebook.com/me?fields=id,name,email,picture{url}')
    profile = resp.json()
    print("Facebook User ", profile)
    return redirect('/')
 


   
@app.route('/instagram/')
def instagram():
   
    # Instagram Oauth Config
    INSTAGRAM_CLIENT_ID = os.environ.get('INSTAGRAM_CLIENT_ID')
    INSTAGRAM_CLIENT_SECRET = os.environ.get('INSTAGRAM_CLIENT_SECRET')
    oauth.register(
        name='instagram',
        client_id=INSTAGRAM_CLIENT_ID,
        client_secret=INSTAGRAM_CLIENT_SECRET,
        request_token_url='https://api.instagram.com/oauth/request_token',
        request_token_params=None,
        access_token_url='https://api.instagram.com/oauth/access_token',
        access_token_params=None,
        authorize_url='https://api.instagram.com/oauth/authenticate',
        authorize_params=None,
        api_base_url='https://api.instagram.com/1.1/',
        client_kwargs=None,
    )
    redirect_ur = url_for('instagram_auth', _external=True)
    return oauth.instagram.authorize_redirect(redirect_ur)
 
@app.route('/instagram/auth/')
def instagram_auth():
    token = oauth.instagram.authorize_access_token()
    resp = oauth.instagram.get('account/verify_credentials.json')
    profile = resp.json()
    print(" instagram User", profile)
    return redirect('/')
 
camera = cv2.VideoCapture(0)  # Use 0 for the default webcam
camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


def analyze_and_render(frame):
    """Analyze a frame and overlay analysis results with rectangles."""
    try:
        # Detect and analyze faces
        analysis_results = DeepFace.analyze(frame, actions=['emotion', 'age'], enforce_detection=False)

        for result in analysis_results:
            # Extract face region and results
            x, y, w, h = result['region']['x'], result['region']['y'], result['region']['w'], result['region']['h']
            emotion = result['dominant_emotion']
            age = int(result['age'])
            # gender = result['gender']

            # Draw rectangle around the face
            start_point = (x, y)
            end_point = (x + w, y + h)
            cv2.rectangle(frame, start_point, end_point, (0, 255, 0), 2)

            # Add text overlay
            text = f"{age}yrs, {emotion}"
            cv2.putText(frame, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2, cv2.LINE_AA)

    except Exception as e:
        # Handle cases where no face is detected
        cv2.putText(frame, "No Face Detected", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)

    return frame

@app.route('/video_feed')
def video_feed():
    """Stream the video feed with real-time analysis."""
    def generate_frames():
        while True:
            success, frame = camera.read()
            if not success:
                break

            # Analyze and render the frame
            frame = analyze_and_render(frame)

            # Encode frame as JPEG
            _, buffer = cv2.imencode('.jpg', frame)
            frame = buffer.tobytes()

            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route("/", methods=["GET", "POST"])
def index():
    processed_image = None
    filename = None
    original_filepath = None

    if request.method == "POST":
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            original_filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(original_filepath)

            # Get user inputs for image processing
            width = request.form.get("width", type=int)
            height = request.form.get("height", type=int)
            angle = request.form.get("angle", type=int)
            flip = request.form.get("flip", type=str)
            blur = request.form.get("blur", type=int)
            contrast = request.form.get("contrast", type=float, default=1.0)
            filter_option = request.form.get("filter", type=str)  # Grayscale or Sepia

            # Read the uploaded image
            img = cv2.imread(original_filepath)

            # Resize the image if dimensions are provided
            if width and height:
                img = cv2.resize(img, (width, height))

            # Rotate the image if an angle is provided
            if angle:
                (h, w) = img.shape[:2]
                center = (w // 2, h // 2)
                matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
                img = cv2.warpAffine(img, matrix, (w, h))

            # Apply blur if specified
            if blur:
                img = cv2.GaussianBlur(img, (blur, blur), 0)

            # Apply flip if specified
            if flip == 'horizontal':
                img = cv2.flip(img, 1)
            elif flip == 'vertical':
                img = cv2.flip(img, 0)

            # Adjust contrast if specified
            if contrast != 1.0:
                img = cv2.convertScaleAbs(img, alpha=contrast, beta=0)

            # Apply filters (Grayscale, Sepia)
            if filter_option == 'grayscale':
                img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            elif filter_option == 'sepia':
                img = cv2.applyColorMap(img, cv2.COLORMAP_PINK)

            # Save the processed image
            processed_filename = f"processed_{filename}"
            processed_filepath = os.path.join(app.config['EDITED_FOLDER'], processed_filename)
            cv2.imwrite(processed_filepath, img)

            # Convert processed image to send to the browser
            processed_image = Image.open(processed_filepath)
            processed_image = processed_image.convert("RGB")
            img_byte_arr = io.BytesIO()
            processed_image.save(img_byte_arr, format='PNG')
            img_byte_arr = img_byte_arr.getvalue()

            return render_template("index.html", processed_image=img_byte_arr, filename=processed_filename, original_filepath=original_filepath)

    return render_template("index.html", processed_image=processed_image, filename=filename, original_filepath=original_filepath)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == "__main__":
    app.run(debug=True)