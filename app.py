from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        #dont want this to be left blank
        content = db.Column(db.String(200), nullable=False)
        date_created = db.Column(db.DateTime, default=datetime.utcnow)

#whenever we make a task it will return the id of the task
        def __repr__(self):
                return '<Task %r>' % self.id

@app.route('/', methods=['POST', 'GET'])

def index():
        if request.method == 'POST':
                #grab task and add to database
                #return 'Hello'
                #task content is equal to the input
                task_content = request.form['content']
                new_task = Todo(content = task_content)

                #push it to our db
                try:
                        db.session.add(new_task)
                        db.session.commit()
                        return redirect('/')
                #if try fails give this error
                except:
                        return 'There was an issue adding your task'
        else:
                tasks = Todo.query.order_by(Todo.date_created).all()
                #pass to our template
                return render_template('index.html', tasks=tasks)
        #return "Hello World"
        
@app.route('/delete/<int:id>')
def delet(id):
        task_to_delete = Todo.query.get_or_404(id)

        try:
                db.session.delete(task_to_delete)
                db.session.commit()
                return redirect('/')
        except:
                return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods = ['GET', 'POST'])
def update(id):
        task = Todo.query.get_or_404(id)
        
        if request.method == 'POST':
               pass
        else:
                return render_template('update.html')


if __name__ == "__main__":
        app.run(debug=True)
