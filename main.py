from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    desc = db.Column(db.Text)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route('/', methods = ["POST", "GET"])
def front():
    if request.method == 'GET':
        tasklist = Task.query.order_by(Task.id).all()
        return render_template('front.html', tasklist=tasklist)


@app.route('/create-task', methods = ["POST", "GET"])
def create():
    if request.method == 'GET':
        return render_template('create-task.html')
    name = request.form.get('task-name')
    desc = request.form.get('task-desc')
    task = Task(name=name, desc=desc)
    
    try:
        db.session.add(task)
        db.session.commit()
        return redirect('/')
    except:
        return 'ОШИБКА'
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)