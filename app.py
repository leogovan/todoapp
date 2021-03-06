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

"""
################################

######### Class Models #########

################################
"""

class Todo(db.Model):
    """
    Class to create a Todo item record in the DB.
    Items will hold the reference back to the parent TodoList.
    """
    __tablename__ = 'todos'
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String, nullable=False)
    completed = db.Column(db.Boolean, nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey('todolists.id'), nullable=False)

    def __repr__(self):
        return f'<Todo {self.id} {self.description}>'


class TodoList(db.Model):
    """
    Class to create a list that will have Todo items related to it in the DB.
    """
    __tablename__ = 'todolists'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(), nullable=False)
    todos = db.relationship('Todo', backref='list', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<TodoList {self.id} {self.name}>'


"""
################################

######## Route handlers ########

################################
"""

"""
######## Create Record Router ########
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
        # targeting the 'description' key in the resulting json that comes from the front end POST
        description = request.get_json()['description']
        # description/completed is now used to create a new Todo() object
        todo = Todo(description=description, completed=False)
        # we use db.session to add that record to the database as it's currently pending
        db.session.add(todo)
        # before the transaction is committed, we can flush this and get the TOBE record id... we couldn't do this until now
        db.session.flush()
        # store the record's id
        todo_id = todo.id
        # we need to commit the transaction (flushes and commits)
        db.session.commit()
        # set a key/value of body to be {description: todo.description}
        body['description'] = todo.description
        # set a key/value of body to be {id: todo_id}
        body['id'] = todo_id
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
        print('I am body before being returned to the view', body)
        return jsonify(body)


"""
######## Update Record Router ########
"""
# Created a route to handle the input from the checkbox
# using <todo_id> with the brackets allows us to parametise that value and use it in our function
@app.route('/todos/<todo_id>/set-completed', methods=['POST'])
# functions that passes in the todo_id captured from the checkbox data-id attribute
def set_completed_todo(todo_id):
    try:
        # completed is the true/false value captured from the event on the front end
        completed = request.get_json()['completed']
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

"""
######## Delete Record Router ########
"""

@app.route('/todos/<button_id>/delete-record', methods=['POST'])
def delete_record(button_id):
    try:
        todo = Todo.query.get(button_id)
        db.session.delete(todo)
        db.session.commit()
    except:
        db.session.rollback()
    finally:
        db.session.close()
    return redirect(url_for('index'))


"""
######## Read Records Router ########
"""

@app.route('/lists/<list_id>')
def get_list_todos(list_id):
    # flask allows us to pass in variables that we want to use in our template
    # here, we pass in 'todo' (it could be called anything) which stores the list of all todo records
    # using Jinja, this will pass to index.html
    return render_template('index.html', 
    # render the list of lists
    lists=TodoList.query.all(),
    active_list=TodoList.query.get(list_id),
    # render the data for the todo items in the list
    todos=Todo.query.filter_by(list_id=list_id).order_by('id').all())


# the index route has been updaed to redirect to get_list_todos()
# also uses list_id=1 just to set the loading default of which list to populate first
@app.route('/')
def index():
    return redirect(url_for('get_list_todos', list_id=1))