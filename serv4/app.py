from flask import Flask,request,render_template,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root@db/test_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = '12345'
db = SQLAlchemy(app)
app.app_context().push()

class Tasks(db.Model):
    id = db.Column("id",db.Integer, primary_key=True)
    title = db.Column("title",db.String(100))
    stack = db.Column("stack",db.String(120))
    mentors = db.Column("mentors",db.String(120))
    user_id = db.Column("user_id",db.Integer, db.ForeignKey('users.id'))    

    def __init__(self,title,stack,mentors,user_id):
        self.title = title
        self.stack = stack
        self.mentors = mentors
        self.user_id = user_id
        
class Users(db.Model):
    id = db.Column("id",db.Integer, primary_key=True)
    username = db.Column("username",db.String(100),unique=True)
    password = db.Column("password",db.String(100))
    tasks = db.relationship('Tasks',backref='user')
    
    def __init__(self,username,password):
        self.username = username
        self.password = password


@app.route("/<id>",methods=["POST","GET"])
def getTasks(id):
    if request.method=="POST":
        title = request.form['title']
        stack = request.form['stack']
        mentor = request.form['mentors']
        task = Tasks(title=title,stack=stack,mentors=mentor,user_id=id)
        db.session.add(task)
        db.session.commit()
        return redirect(url_for("viewTasks",id=id))
    user = Users.query.filter_by(id=id).first()
    return render_template("index.html",user = user)

@app.route("/tasks/<id>")
def viewTasks(id):
    tasks = Tasks.query.filter_by(user_id=id).all()
    return render_template("tasks.html",content = {'tasks':tasks,'count': len(tasks),'update':0})

@app.route("/delete/<id>/<tid>")
def delete(id,tid):
    Tasks.query.filter_by(id=tid).delete()
    db.session.commit()
    tasks = Tasks.query.filter_by(user_id=id).all()
    return render_template("tasks.html",content = {'tasks':tasks,'count':len(tasks),'update':0})

@app.route("/update/<id>/<tid>",methods=["POST","GET"])
def update(id,tid):
    if request.method=="POST":
        task_to_update = Tasks.query.filter_by(id=tid).first()
        task_to_update.title = request.form['title']
        task_to_update.stack = request.form['stack']
        task_to_update.mentors = request.form['mentors']
        db.session.commit()
        return redirect(url_for('viewTasks',id=id))    
    task_to_update = Tasks.query.filter_by(id=tid).first()
    print(type(task_to_update.id))
    print(type(4))
    tasks = Tasks.query.filter_by(user_id=id).all()
    return render_template("tasks.html",content = {'tasks':tasks,'count': len(tasks),'update':task_to_update.id})
    
    

if __name__=="__main__":
    app.run(debug=True)

