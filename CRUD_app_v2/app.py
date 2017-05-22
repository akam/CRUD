from flask import Flask, redirect, url_for, render_template, request
from flask_modus import Modus
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
modus = Modus(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/users_ex'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    
    __tablename__ = "users" # table name will default to name of the model

    # Create the three columns for our table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, unique=True,nullable=False)
    email = db.Column(db.Text, unique=True,nullable=False)
    first_name = db.Column(db.Text)
    last_name = db.Column(db.Text)
    messages = db.relationship('Message', backref='user', lazy='dynamic')

    # define what each instance or row in the DB will have (id is taken care of for you)
    def __init__(self, first_name, last_name, username, email):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name

    # this is not essential, but a valuable method to overwrite as this is what we will see when we print out an instance in a REPL.
    def __repr__(self):
        return "The User's name is {} {}".format(self.first_name, self.last_name)

class Message(db.Model):

    __tablename__ = "messages"

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.VARCHAR(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, message, user_id):
        self.message = message
        self.user_id = user_id

@app.route('/')
def base():
    return redirect(url_for('index'))

@app.route('/users')
def index():
    all_users = User.query.all()
    return render_template('index.html', all_users=all_users)

@app.route('/users', methods=["POST"])
def create():
    new_user = User(request.form['first_name'], request.form['last_name'],request.form['username'], request.form['email'])
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/users/new')
def new():
    return render_template('new.html')

@app.route('/users/<int:id>/edit')
def edit(id):
    user = User.query.get(id)
    return render_template('edit.html', user=user)


@app.route('/users/<int:id>', methods=["GET", "PATCH", "DELETE"])
def show(id):
    user = User.query.get_or_404(id)
    if request.method == b"DELETE":
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for('index'))
    if request.method == b"PATCH":
        user.username = request.form['username']
        user.email = request.form['email']
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('show', id = user.id))    
    return render_template('show.html', user = user)

@app.route('/users/<int:id>/messages')
def message_index(id):
    # from IPython import embed; embed()
    return render_template('message_index.html', user=User.query.get(id), all_messages=User.query.get(id).messages)

@app.route('/users/<int:id>/messages/new')
def message_new(id):
    return render_template('message_new.html', user=User.query.get(id))

@app.route('/users/<int:id>/messages', methods=["POST"])
def message_create(id):
    new_message = Message(request.form['message_text'], id)
    db.session.add(new_message)
    db.session.commit()
    return redirect(url_for('message_index', id=id))

@app.route('/users/<int:id>/messages/<int:mid>', methods=["PATCH", "DELETE"])
def message_show(id, mid):
    if request.method == b"PATCH":
        edit = Message.query.get(mid)
        edit.message = request.form['edited_message']
        db.session.add(edit)
        db.session.commit()
        return redirect(url_for('message_index', id=id))
    if request.method == b"DELETE":
        delete_msg = Message.query.get(mid)
        db.session.delete(delete_msg)
        db.session.commit()
        return redirect(url_for('message_index', id=id))
    

@app.route('/users/<int:id>/messages/edit')
def message_edit(id):
    return render_template('message_edit.html', user=User.query.get(id), all_messages=User.query.get(id).messages.all())






if __name__ == '__main__':
    app.run(debug=True,port=3000)