"""Blogly application."""

from turtle import position
from flask import Flask,render_template,request,redirect,flash
from models import db, connect_db,User,Post
from flask_toastr import Toastr

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:0258@localhost:5432/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True



from flask_debugtoolbar import DebugToolbarExtension
app.config['SECRET_KEY'] = "SECRET!"
app.config[' DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

toastr = Toastr(app)


# Get list of all Users
@app.route('/')
def home():
    users = User.query.all()
    return render_template("home.html",users=users)

# Get info of the User based on ID from DB
@app.route('/<int:user_id>')
def find_user(user_id):
    user = User.query.get(user_id)
    if user is None:
        flash("There is no such user")
        return redirect("/")
    post = Post.query.filter_by(user_id=user_id)
    return render_template("user-info.html", user=user,post=post)

# Get the add-user Form
@app.route("/add-user")
def add_user():
    return render_template("add-user.html")

# Get info from add-user Form
@app.route("/add-user", methods=["POST"])
def create_user():
    first = request.form["first_name"]
    last = request.form["last_name"]
    image = request.form["image_url"] or None
   

    user = User(first_name = first, last_name = last, image_url = image)
    db.session.add(user)
    db.session.commit()
    flash("User successfully added ")

    return redirect("/")

# Get /edit form from edit.html
@app.route('/edit/<int:user_id>')
def edit_user(user_id):
    user = User.query.get(user_id)
    return render_template("edit.html",user=user)
    
# Get info from edit-form   
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
    flash("User successfully updated ")
    return redirect("/")

# Delete user from DB
@app.route('/delete/<int:user_id>', methods=["POST"])
def users_destroy(user_id):
    
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash("User {user successfully removed ")

    return redirect("/")

###########################################################################
##########################################################################

# Get info from POST
@app.route('/<user_id>/posts/new')
def get_posts(user_id):
    user = User.query.get(user_id)
    print(user)
    if user is None:
        flash(f"No user '{user_id}' found.")
        return redirect("/")
    return render_template("posts.html",user=user)

# Get the data and add it to DB
@app.route('/<user_id>/posts/new', methods=["POST"])
def show_post(user_id):
    user = User.query.get_or_404(user_id)
    title = request.form["title"]
    content = request.form["postBody"]

    if user is not None:
        post = Post(title = title, content=content, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        flash(f"Post '{post.title}' added.")
        return redirect(f"/{user.id}")

    flash(f"Invalid user {user_id}")
    return redirect("/")
    

# Display a specific post
@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    post = Post.query.get_or_404(post_id)
    if post is not None:
        user = User.query.get(post.user_id)
    else:
        return redirect("/")
        flash('Post not found')
    return render_template("showposts.html", user=user , post=post)

# Get the form from edit-post.html
@app.route('/posts/<int:post_id>/edit')
def show_edit_page(post_id):
    post = Post.query.get(post_id)
    return render_template("edit-post.html",post=post)


# Edit and Submit the specific post
@app.route('/posts/<int:post_id>/edit',methods=["POST"])
def submit_edit_page(post_id):
    post = Post.query.get(post_id)
    post.title = request.form["title"]
    post.content = request.form["postBody"]
    
    db.session.add(post)
    db.session.commit()
    flash("Post successfully updated ")
    
    return redirect(f"/posts/{post.id}")
    
# Delete specific post
@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def posts_destroy(post_id):
    

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()
    flash(f"Post '{post.title} deleted.")

    return redirect("/")