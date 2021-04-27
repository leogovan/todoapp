from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import sys

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://leogovan@localhost:5432/todoapp'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# links to instance of our Flask app and our SQLAlchemy database
migrate = Migrate(app, db)

class Todo(db.Model):
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    completed = db.Column(db.Boolean, nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'

"""
#### Route handlers ###
"""

# Created new route to handle the text form input field (routing to creating a new record in the todos table)
# '/todos/create' is setting the definition for the form to connect with
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
        # description/completed is now used to create a new Todo() object
        todo = Todo(description=description, completed=False)
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

# Created a route to handle the input from the checkbox
# using <todo_id> with the brackets allows us to parametise that value and use it in our function
@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
# functions that passes in the todo_id captured from the checkbox data-id attribute
def set_completed_todo(todo_id):
    try:
        print("I am todo_id", todo_id)
        # completed is the true/false value captured from the event on the front end
        completed = request.get_json()['completed']
        print("I am completed: ", completed)
        # gets the object from the db by its primary key
        todo = Todo.query.get(todo_id)
        # set the object's completed property to the value of the completed variable
        todo.completed = completed
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    #### DO I REALLY WANT TO REFRESH? SURELY I WANT TO AJAX EVERYTHING? ####
    return redirect(url_for('index'))


@app.route('/')
def index():
    # flask allows us to pass in variables that we want to use in our template
    # here, we pass in 'data' which stores the list of all todo records
    # using Jinja, this will pass to index.html
    print("Lalala", Todo.query.order_by('id').all())
    return render_template('index.html', data=Todo.query.order_by('id').all())