
# from distutils.log import debug
# from email.policy import default
#from asyncio import tasks
#from crypt import methods
#import re
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, redirect,render_template, request,url_for 
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class ToDO(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(250), nullable=False)
    #completted = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return '<Task %r>' % self.id



@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        task_content = request.form['content']
        new_task = ToDO(content=task_content)
        
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue adding the task"

    else:
        tasks = ToDO.query.order_by(ToDO.date_created).all()

        return render_template('index.html',tasks = tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = ToDO.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return "There was a problem deleting the task"


@app.route('/update/<int:id>',methods=['POST','GET'])
def update(id):
    
    task_to_update = ToDO.query.get_or_404(id)
    if request.method=="POST":
        task_to_update.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return "There was an issue updating the task"
    else:
        return render_template('update.html',task = task_to_update)
    return redirect()


if __name__=="__main__":
    app.run(debug=True) 