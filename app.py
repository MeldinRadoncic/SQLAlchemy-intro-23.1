"""Blogly application."""

from turtle import position
from flask import Flask,render_template,request,redirect,flash
from models import db, connect_db,User,Post,Tag,PostTag
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
    tag = Tag.query.all()
    return render_template("user-info.html", user=user,post=post,tag=tag)


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

########################################################################
########################################################################

# TAGS

# Getting form form add-tag.html
@app.route('/<int:user_id>/tag/new')
def get_add_tag(user_id):
    user = User.query.get(user_id)
    posts = Post.query.all()
    return render_template("add-tag.html", user=user,posts=posts)

# Getting Data from add-tag.html form
@app.route('/<int:user_id>/tag/new', methods=["POST"])
def post_tag(user_id):
    name = request.form["tagName"]
    user = User.query.get(user_id)
    
    if user is not None:
        tag = Tag(name = name)
        db.session.add(tag)
        db.session.commit()
        flash(f"Tag '{tag.name}' added.")
        return redirect(f"/{user.id}")
    else:
        flash(f"Invalid user {user_id}")
        return redirect("/")

# Show all the tags 
@app.route('/tag/<int:tag_id>')
def show_tags(tag_id):
    
    tag = Tag.query.get_or_404(tag_id)
    return render_template("/show-tags.html", tag=tag)

# Show edit-tag page
@app.route('/tag/<int:tag_id>/edit')
def edit_tags_form(tag_id):
    tag = Tag.query.get(tag_id)
    posts = Post.query.all()
    return render_template("edit-tags.html", tag=tag, posts=posts)

  # Update and save changes on tag      
@app.route('/tag/<int:tag_id>/edit', methods=["POST"])
def tags_edit(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()
    if tag is not None:
        db.session.add(tag)
        db.session.commit()
        flash(f"Tag '{tag.name}' edited.")
        return redirect("/")
    else:
        flash("Tag not found")
        return redirect('/')

# Delete tag
@app.route('/tag/<int:tag_id>/delete', methods=["POST"])
def tags_destroy(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' deleted.")

    return redirect("/")
