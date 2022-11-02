from flask import Flask;
from flask import render_template;
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def page():
 return render_template('page.html')

@app.route("/home")  
def home():
  return render_template('home.html')

@app.route("/about")  
def about():
  return render_template('about.html')

@app.route('/signin')
def signin():
    return render_template('signin.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')