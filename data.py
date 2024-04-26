from distutils.log import debug
from flask import Flask,render_template,request
from urllib.request import urlopen as uReq
from parth import readfile
from flask_sqlalchemy import SQLAlchemy
import datetime
from fileinput import filename
from flask import *
import os
from werkzeug.utils import secure_filename
from summarizer import summarize

data={}
UPLOAD_FOLDER='C:\\Users\\Lenovo\\Desktop\\ProjectMaster'

db = SQLAlchemy()
app=Flask(__name__,template_folder="templates")
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://root:@localhost/textsummarizer"
app.config['SECRET_KEY'] = 'the random string'


db.init_app(app)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

class User(db.Model):
    SrNo = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(30), nullable=False)
    Password=db.Column(db.String(30),nullable=False)
    date=db.Column(db.Date)

@app.route("/")
def main():
    return render_template("summerizer.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/text")
def func():
    return render_template("nofile.html")


@app.route("/login",methods=['GET','POST'])
def log():
    if request.method=='POST':
        name=request.form.get('usrn')
        password=request.form.get('pass')

        entry=User(Username=name,Password=password,date=datetime.datetime.now())
        db.session.add(entry)
        db.session.commit()
        return render_template("summerizer.html")
    


@app.route("/",methods=['GET','POST'])
def read_file():
        if  request.method=='POST':
                    file = request.files['file']
                    if file.filename!='':
                        filename = secure_filename(file.filename)
                        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                        data['first']=readfile(filename)
                        file.filename=''
                        return redirect(url_for('inp'))

                    elif file.filename=='':
                            inputd=request.form['inpdata']
                            text=summarize(inputd)
                            return render_template('summerizer.html',data=inputd,it=text)


@app.route('/download')
def filet():
    path = "C:/Users/Lenovo/Desktop/ProjectMaster/Summary.txt"
    return send_file(path, as_attachment=True)

@app.route("/input")
def inp():
    return render_template("index.html",info=data['first'])


@app.route("/input",methods=['POST'])
def summmary():
    if request.method=='POST':
        data=request.form['in']
        text=summarize(data)
        return render_template("index.html", info=data,Summary=text)
            
if __name__=="__main__":
    app.run(debug=True,host="0.0.0.0",threaded=True)
    
    