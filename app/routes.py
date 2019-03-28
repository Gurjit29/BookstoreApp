from flask import render_template,flash,redirect
from app import app
from app.forms import LoginForm,RegistrationForm
from flask_login import current_user, login_user
from app import db
from app.models import User,Post,Book
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse

@app.route('/')
@app.route('/index')
#..@login_required
def index():
   posts=Post.query.all()
   books=Book.query.all()
   if current_user.is_authenticated:
     return render_template("index.html", title='Home Page',books=books, posts=posts)
   return render_template("preview.html",title='Preview',books=books,posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect('/index')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect('/login')
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = '/index'
       	    return redirect(next_page)
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
	logout_user()
	return redirect('/index')

@app.route('/book')
def book():
   id=request.args.get('id')
   posts=Post.query.all()
   book=Book.query.get(id)
   return render_template('book.html',posts=posts,book=book,id=int(id))

@app.route('/delete')
@login_required
def delete():
     id=request.args.get('id')
     post=Post.query.get(id)
     db.session.delete(post)
     db.session.commit()
     return redirect('/index')   

@app.route('/add', methods=['POST'])
def add():
     
     body=request.form['body']
     users=User.query.all()
     for u in users:
        if u.username == current_user.username:
           newPost=Post(body=body,author=u)
           db.session.add(newPost)
           db.session.commit()
           break;
     return redirect ('/index')

@app.route('/update')
@login_required
def update():
    id=request.args.get('id')
    posts=Post.query.all()
    return render_template('update.html',posts=posts,id=int(id))
 


@app.route('/modify',methods=['POST'])
@login_required
def modify():
    id=request.args.get('id')
    body=request.form['body']
    post=Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    user=User.query.filter_by(username=current_user.username).first()
    post=Post(body=body,id=id,author=user)
    db.session.add(post)
    db.session.commit()
    return redirect('/index') 

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect("/login")
    return render_template('register.html', title='Register', form=form)        
