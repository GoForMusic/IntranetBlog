import secrets
import os
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from mainblog import app, db, bcrypt
from mainblog.forms import RegistrationForm, LoginForm, UpdateProgileForm, PostForm
from mainblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required




#route with every functions
@app.route("/")
@app.route("/home")
def home_page():
    posts = Post.query.all()
    return render_template('home.html', posts=posts)


@app.route("/about")
def about_page():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'{ form.email.data }! was created', 'success')
        return redirect(url_for('login_page'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for('home_page'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home_page'))
        else:
            flash('Login Unsuccessful. Please check the credentials', 'danger')
    return render_template('login.html', title='Login', form=form)


@app.route("/logout")
def logout_page():
    logout_user()
    return redirect(url_for('home_page'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route("/account", methods=['GET', 'POST'])
@login_required
def account_page():
    form = UpdateProgileForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.email = form.email.data
        current_user.firstname = form.firstname.data
        current_user.lastname = form.lastname.data
        db.session.commit()
        flash('Your account has benn updated!', 'success')
        return redirect(url_for('account_page'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.firstname.data = current_user.firstname
        form.lastname.data = current_user.lastname
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('account.html', title='Account', avatar=image_file, user=current_user, form=form)



@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post_page():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home_page'))
    return render_template('create_post.html', title='New Post', form=form)

@app.route("/post/<string:post_id>", methods=['GET', 'POST'])
def post_page(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<string:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post_page(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash(f'Your post (id: { post_id }) has been updated!', 'success')
        return redirect(url_for('post_page', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form)


@app.route("/post/<string:post_id>/delete", methods=['POST', 'DELETE'])
@login_required
def delete_post_page(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    flash(f'Your post (id: { post_id }) has been deleted!', 'success')
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('home_page'))
    

