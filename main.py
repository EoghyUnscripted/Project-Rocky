"""

"""

from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_bootstrap import Bootstrap
from flask_ckeditor import CKEditor
from datetime import date
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
from forms import CreateBlogPostForm, CreateStatusUpdateForm, RegisterForm, LoginForm, CommentForm, ContactForm, send_email, EditProfileForm
from flask_gravatar import Gravatar
from functools import wraps
from datetime import datetime
import os
from decouple import config

# Initialize Flask App & Config
app = Flask(__name__)

# Flask App Configurations
app.config['SECRET_KEY'] = config('FLASK_SECRET_KEY')
login_manager = LoginManager()

# Initialize Gravatar Image Object
gravatar = Gravatar(app,
                    size=100,
                    rating='g',
                    default='retro',
                    force_default=False,
                    force_lower=False,
                    use_ssl=False,
                    base_url=None)

# Database Connector
app.config['SQLALCHEMY_DATABASE_URI'] = config('DB_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize App Modules
ckeditor = CKEditor(app)
Bootstrap(app)
db = SQLAlchemy(app)
login_manager.init_app(app)

# Set Variables
this_year = datetime.now().year

# Flask Login Loader
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Admin route decorator function
def admin_only(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        # If id is not 1 then return abort with 403 error
        if current_user.id != 1:

            return abort(403)

        # Otherwise continue with the route function
        return f(*args, **kwargs)

    return decorated_function


# Initialize User Class For Database Table
class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    catch_phrase = db.Column(db.String, nullable=True)
    body = db.Column(db.Text, nullable=True)
    
    # Relationship Links
    posts = relationship("BlogPost", back_populates="author")
    comments = relationship("Comment", back_populates="comment_author")
    
    def __repr__(self):
        return '<User %r>' % self.email

# Initialize Character Class For Database Table
class Character(db.Model):
    __tablename__ = "characters"
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    name = db.Column(db.String(100))
    catch_phrase = db.Column(db.String(100))
    body = db.Column(db.String(1000))

# Initialize Blog Post Class For Database Table
class BlogPost(db.Model):
    __tablename__ = "posts"
    id = db.Column(db.Integer, primary_key=True)    
    title = db.Column(db.String(250), unique=True, nullable=False)
    subtitle = db.Column(db.String(250), nullable=False)
    date = db.Column(db.String(250), nullable=False)
    body = db.Column(db.Text, nullable=False)
    img_url = db.Column(db.String(250), nullable=False)
    
    # Relationship Links
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="parent_post")
    
# Initialize Blog Comment Class For Database Table
class Comment(db.Model):
    __tablename__ = "comments"
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    comment_author = relationship("User", back_populates="comments")
    
    # Relationship Links 
    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"))
    parent_post = relationship("BlogPost", back_populates="comments")
    text = db.Column(db.Text, nullable=False)
    
# Create Database with Tables
db.create_all()

# Main app route
@app.route('/', methods=['GET', 'POST'])
def get_all_posts():

    # Access all posts from database table
    posts = BlogPost.query.all()

    # If user not logged in
    if not current_user.is_authenticated:

        # Message to display on login screen
        flash("Please log in or register.")

        # Reload login.html with message
        return redirect(url_for("login"))

    else:

        # Render index with posts, and current user data
        return render_template("index.html", all_posts=posts, current_user=current_user, year=this_year)

# Registration app route
@app.route('/register', methods=['GET', 'POST'])
def register():

    form = RegisterForm()   # Create WTF registration form

    # On POST
    if form.validate_on_submit():

        # Check if user exists
        if User.query.filter_by(email=form.email.data).first():

            # Message to display on login screen
            flash("You've already signed up with that email, log in instead!")

            # Redirect to login.html
            return redirect(url_for('login'))

        # If new user, hash and salt password
        hash_and_salted_password = generate_password_hash(
            form.password.data,
            method='pbkdf2:sha256',
            salt_length=8
        )

        # Create new user object with hashed password
        new_user = User(
            email=form.email.data,
            password=hash_and_salted_password,
            name=form.name.data,
            catch_phrase=form.catch_phrase.data,
            body=form.body.data
        )

        # Add record to database table
        db.session.add(new_user)
        db.session.commit()

        # Log in user in app
        login_user(new_user)

        # Redirect to index.html
        return redirect(url_for('get_all_posts'))

    # If GET, render registration page with form
    return render_template("register.html", form=form, current_user=current_user, year=this_year)

# Login app route
@app.route('/login', methods=['GET', 'POST'])
def login():

    form = LoginForm()  # Create WTF login form

    # On POST
    if form.validate_on_submit():

        # Get form data
        email = form.email.data
        password = form.password.data

        # Check if email in database table
        user = User.query.filter_by(email=email).first()

        # If no existing user
        if not user:

            # Message to display on login screen
            flash("That email does not exist, please try again.")

            # Reload login.html with message
            return redirect(url_for('login'))

        # If user exists, and incorrect password
        elif not check_password_hash(user.password, password):

            # Message to display on login screen
            flash('Password incorrect, please try again.')

            # Reload login.html with message
            return redirect(url_for('login'))

        # If successful
        else:

            login_user(user)    # Log in user in app

            # Redirect to index.html
            return redirect(url_for('get_all_posts'))

    # If GET, render login page with form
    return render_template("login.html", form=form, current_user=current_user, year=this_year)

# Logout app route
@app.route('/logout')
@login_required
def logout():

    logout_user()   # Log user out of app

    # Redirect to index.html
    return redirect(url_for('get_all_posts'))

# Show Post app route
@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def show_post(post_id):

    form = CommentForm()    # Create WTF comment form

    # Get blog post by id from database table
    requested_post = BlogPost.query.get(post_id)
    print(requested_post)

    # On POST
    if form.validate_on_submit():

        # If user not logged in
        if not current_user.is_authenticated:

            # Message to display on login screen
            flash("You need to login or register to comment.")

            # Reload login.html with message
            return redirect(url_for("login"))

        # Create new comment object
        new_comment = Comment(
            text=form.comment.data,
            comment_author=current_user,
            parent_post=requested_post
        )

        # Add record to database table
        db.session.add(new_comment)
        db.session.commit()

        # Reload page with new comment
        return redirect(url_for("show_post", post_id=requested_post.id))

    # If GET, render show_post page with form, blog post data, and current user data
    return render_template("post.html", post=requested_post, form=form, current_user=current_user, year=this_year)

# About app route
@app.route("/profile")
def show_profile():

    if current_user.is_authenticated:
        
        print(current_user)

        # Load User Profile
        return render_template("profile.html", current_user=current_user, year=this_year)

    else:

        # Redirect to index.html
        return redirect(url_for('get_all_posts'))

# Edit profile app route
@app.route("/edit-profile/", methods=['GET', 'POST'])
@login_required
def edit_profile():

    # Get profile record by id from database table
    profile = current_user

    # Create WTF post form and prefill with existing user data
    edit_form = EditProfileForm(
        name=profile.name,
        email=profile.email,
        catch_phrase=profile.catch_phrase,
        body=profile.body
    )

    # On POST
    if edit_form.validate_on_submit():

        # Get form data
        profile.name = edit_form.name.data
        profile.email = edit_form.email.data
        profile.catch_phrase = edit_form.catch_phrase.data
        profile.body = edit_form.body.data

        # Update record in database table with new data
        db.session.commit()

        # Redirect to the show_profile.html with new edits
        return redirect(url_for("show_profile"))

    # If GET, render edit profile form, and current user data
    return render_template("make-profile.html", form=edit_form, current_user=current_user, is_edit=True, year=this_year)

# Contact app route
@app.route("/contact", methods=['GET', 'POST'])
def contact():

    form = ContactForm()    # Create WTF contact form

    # On POST
    if form.validate_on_submit():

        # Variables
        name = form.name.data
        email = form.email.data
        message = form.message.data

        # Check if email sent successfully
        if send_email(name, email, message):

            # Message to display on login screen
            flash("Your message was sent, successfully!")

            # Refresh contact.hmtl with message
            return redirect(url_for("contact"))

        # If failed
        else:

            # Message to display on login screen
            flash("Your message could not be sent at this time, try again, later!")

            # Refresh contact.hmtl with message
            return redirect(url_for("contact"))

    # If GET, render contact.html with form, and current user data
    return render_template("contact.html", form=form, current_user=current_user, year=this_year)

# Add new post app route
@app.route("/new-post", methods=['GET', 'POST'])
@login_required
def add_new_post():

    form = CreateBlogPostForm()     # Create WTF new blog post form

    # On POST
    if form.validate_on_submit():

        # Create new blog post object
        new_post = BlogPost(
            title=form.title.data,
            subtitle=form.subtitle.data,
            body=form.body.data,
            img_url=form.img_url.data,
            author=current_user,
            date=date.today().strftime("%B %d, %Y")
        )

        # Add record to database table
        db.session.add(new_post)
        db.session.commit()

        # Redirect to index.html
        return redirect(url_for("get_all_posts"))

    # If GET, render new blog form, and current user data
    return render_template("make-post.html", form=form, current_user=current_user, is_edit=False, year=this_year)

# Edit post app route
@app.route("/edit-post/<int:post_id>", methods=['GET', 'POST'])
@login_required
def edit_post(post_id):

    # Get blog post record by id from database table
    post = BlogPost.query.get(post_id)

    # Create WTF post form and prefill with existing post data
    edit_form = CreateBlogPostForm(
        title=post.title,
        subtitle=post.subtitle,
        img_url=post.img_url,
        author=post.author,
        body=post.body
    )

    # On POST
    if edit_form.validate_on_submit():

        # Get form data
        post.title = edit_form.title.data
        post.subtitle = edit_form.subtitle.data
        post.img_url = edit_form.img_url.data
        post.author = current_user
        post.body = edit_form.body.data

        # Update record in database table with new data
        db.session.commit()

        # Redirect to the show_post.html with new edits
        return redirect(url_for("show_post", post_id=post.id))

    # If GET, render edit blog post form, and current user data
    return render_template("make-post.html", form=edit_form, current_user=current_user, is_edit=True, year=this_year)

# Delete post app route
@app.route("/delete/<int:post_id>")
@login_required
def delete_post(post_id):

    # Get blog post by id from database table
    post_to_delete = BlogPost.query.get(post_id)

    # Delete record
    db.session.delete(post_to_delete)
    db.session.commit()

    # Redirect to index.html
    return redirect(url_for('get_all_posts'))


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)