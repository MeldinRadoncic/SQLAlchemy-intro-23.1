"""Blogly application."""

from contextlib import redirect_stderr
from flask import Flask,render_template,request,redirect
from models import db, connect_db,User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0258@localhost:5432/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
app.config[' DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


# Get list of all Users
@app.route('/')
def home():
    users = User.query.all()
    return render_template("home.html",users=users)

# Get info of the User based on ID from DB
@app.route('/<user_id>')
def find_user(user_id):
    user = User.query.get(user_id)
    return render_template("user-info.html", user=user)

# Get the add-user Form
@app.route("/add-user")
def add_user():
    return render_template("add-user.html")

# Get info from add-user Form
@app.route("/add-user", methods=["POST"])
def create_user():
    first = request.form["first_name"]
    last = request.form["last_name"]
    image = request.form["image_url"]

    user = User(first_name = first, last_name = last, image_url = image)
    db.session.add(user)
    db.session.commit()

    return redirect("/")

# Get /edit form from edit.html
@app.route('/edit/<int:user_id>')
def edit_user(user_id):
    user = User.query.get(user_id)
    return render_template("edit.html",user=user)
    
# Get info from edit-fprm   
@app.route('/edit/<int:user_id>')
def users_edit(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("/edit.html", user=user)
    
# Get info from edit form and update in the DB
@app.route('/edit/<int:user_id>', methods=["POST"])
def users_update(user_id):
   
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']

    db.session.add(user)
    db.session.commit()

    return redirect("/")

# Delete user from DB
@app.route('/delete/<int:user_id>', methods=["POST"])
def users_destroy(user_id):
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/")
