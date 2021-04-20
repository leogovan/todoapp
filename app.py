from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
import sys

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
    # error is defined at the top to be used below
    error = False
    # initialise teh body disctionary for use below
    body = {}
    # try/except block to handle possible expected exceptions
    try:
        # targeting the 'description' key in the resulting json
        description = request.get_json()['description']
        # description is now used to create a new Todo() object
        todo = Todo(description=description)
        # we use db.session to add that record to the database as it's currently pending
        db.session.add(todo)
        # we need to commit the transaction (flushes and commits)
        db.session.commit()
        print("I am body before", body)
        # set the key/value of body to be {description: todo.description}
        body['description'] = todo.description
        print("I am body after", body)
    except:
        # set error to True if issue is raised
        error = True
        # rollback the session if unsuccessful
        db.session.rollback()
        # using sys module, print the error to the terminal
        print(sys.exc_info())
    finally:
        db.session.close()
    # the if/else block is run regardless of the try/except/finally block
    if error:
        # return an error back to the route handler using abort()
        abort(400)
    else:
        # return the json data back to the view
        return jsonify(body)


@app.route('/')
def index():
    return render_template('index.html', data=Todo.query.all())