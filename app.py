from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://leogovan@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

db.create_all()

# Created new route to handle the form input field (routing to the )
@app.route('/todos/create', methods=['POST'])
# function to create a todo item
def create_todo():
    # targeting the 'description' key in the resulting json
    description = request.get_json()['description']
    # description is now used to create a new Todo() object
    todo = Todo(description=description)
    # we use db.session to add that record to the database as it's currently pending
    db.session.add(todo)
    # we need to commit the transaction (flushes and commits)
    db.session.commit()
    # use the jsonify method to get the value from the...
    return jsonify({
        'description': todo.description
    })

@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())