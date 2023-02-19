from flask import Flask,redirect,url_for,render_template,request,flash,redirect
from flask_sqlalchemy import SQLAlchemy

import os
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@db/test_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '12345'
db = SQLAlchemy(app)
app.app_context().push()


class users(db.Model):
    id = db.Column("id",db.Integer, primary_key=True)
    username = db.Column("username",db.String(100),unique=True)
    password = db.Column("password",db.String(100))
    
    def __init__(self,username,password):
        self.username = username
        self.password = password
        
    def __repr__(self):
        return f"{self.username}"
    

#DEFAULT ROUTE
@app.route("/")
def index():
    return redirect('register')

@app.route("/register",methods=['POST','GET'])
def register():
    if request.method=="POST":
        name = request.form['name']
        password = request.form['pass']
        user = users.query.filter_by(username=name).first()
        if user:
            flash("USERNAME ALREADY EXISTS!")
            return redirect('register')
        user = users(username=name, password=password)
        db.session.add(user)
        db.session.commit()
        flash("REGISTERED SUCCESSFULLY")
        return redirect("login")
    return render_template('register.html')

@app.route("/login",methods=['POST','GET'])
def login():
    if request.method=="POST":
        login_name = request.form['username']
        login_pass = request.form['pass']
        user = users.query.filter_by(username=login_name).first()
        if user:
            if login_pass==user.password:
                return redirect(f"tasks/{user.id}")
            else:
                flash("INVALID PASSWORD")
                return redirect('login')
        else:
            flash("USER DOES NOT EXIST")
            return redirect('login')
    return render_template('login.html')


@app.route("/admin",methods=["POST","GET"])
def deluser():
    if request.method=="POST":
        try:
            db.session.query(users).delete()         
            db.session.commit()
        except:
            db.session.rollback()
        db.session.add(users(username="Girish",password="1234")) 
        db.session.commit()
    return render_template('admin.html')

if __name__=="__main__":
    app.run(debug=True,host='0.0.0.0')