from flask import Flask, render_template, redirect, url_for, request
from flask_modus import Modus
from flask_sqlalchemy import SQLAlchemy
# import db
# from toy import Toy

app = Flask(__name__)
modus = Modus(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://localhost/flask-toys'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Toy(db.Model):
    __tablename__ = "toys"

    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)

    def __init__(self, name):
        self.name = name


# duplo = Toy(name='duplo')
# lego = Toy(name='lego')
# knex = Toy(name='knex')
#
# toys = [duplo,lego,knex]

@app.route('/')
def home():
    return redirect(url_for('index'))

@app.route('/toys', methods=["GET", "POST"])
def index():
    if request.method == "POST":
        from IPython import embed; embed()
        # gather the value of an input with a name attribute of "name"
        db.add_toy(request.form['name'])
        # respond with a redirect to the route which has a function called "index" (in this case that is '/toys')
        return redirect(url_for('index'))

    toys = Toy.query.all()
    return render_template('index.html', toys=toys)

@app.route('/toys/new')
def new():
    return render_template('new.html')

@app.route('/toys/<int:id>', methods=["GET", "PATCH", "DELETE"])
def show(id):
    found_toy = Toy.query.get(id)
    # if we are updating a toy...
    if request.method == b"PATCH":
        found_toy.name = request.form['name']
        db.session.add(found_toy)
        db.session.commit()
        return redirect(url_for('index'))
    if request.method == b"DELETE":
        db.session.delete(found_toy)
        db.session.commit()
        return redirect(url_for('index'))

    return render_template('show.html', toy=found_toy)

@app.route('/toys/<int:id>/edit')
def edit(id):
    # Refactored using a list comprehension!
    found_toy = Toy.query.get(id)
    # Refactor the code above to use a generator so that we do not need to do [0]!
    return render_template('edit.html', toy=found_toy)

if __name__ == '__main__':
    app.run(debug=True,port=3000)



