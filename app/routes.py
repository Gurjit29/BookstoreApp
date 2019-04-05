
from flask import render_template,flash,redirect,url_for
from app import app,mail
from flask_mail import Mail
from flask_mail import Message
from app.forms import LoginForm,RegistrationForm,PasswordResetForm
from flask_login import current_user, login_user
from app import db
from app.models import User,Post,Book
from flask_login import logout_user
from flask_login import login_required
from flask import request
from werkzeug.urls import url_parse
from itsdangerous import URLSafeTimedSerializer
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
   book=Book.query.filter_by(id=id).first()

   return render_template('book.html',posts=posts,book=book,id=int(id))

@app.route('/delete')
@login_required
def delete():
     bookId=request.args.get('bookId')
     id=request.args.get('id')
     post=Post.query.get(id)
     db.session.delete(post)
     db.session.commit()
     posts=Post.query.all()
     book=Book.query.filter_by(id=bookId).first()
     return render_template('book.html',posts=posts,book=book,id=int(bookId))
   

@app.route('/add', methods=['POST'])
def add():
     bookId=request.args.get('bookId')
     book=Book.query.filter_by(id=bookId).first()
     body=request.form['body']
     users=User.query.all()
     for u in users:
        if u.username == current_user.username:
           newPost=Post(body=body,author=u,review=book)
           db.session.add(newPost)
           db.session.commit()
           break;
     posts=Post.query.all()
     return render_template('book.html',posts=posts,book=book,id=int(bookId))

@app.route('/update')
@login_required
def update():
    id=request.args.get('id')
    bookId=request.args.get('bookId')
    posts=Post.query.all()
    book=Book.query.filter_by(id=bookId).first()
    return render_template('update.html',book=book,posts=posts,id=int(id),bookId=int(bookId))
 


@app.route('/modify',methods=['POST'])
@login_required
def modify():
    id=request.args.get('id')
    bookId=request.args.get('bookId')
    body=request.form['body']
    post=Post.query.get(id)
    db.session.delete(post)
    db.session.commit()
    user=User.query.filter_by(username=current_user.username).first()
    book=Book.query.filter_by(id=bookId).first()
    post=Post(body=body,id=id,author=user,review=book)
    db.session.add(post)
    db.session.commit()
    posts=Post.query.all()
    return render_template('book.html',posts=posts,book=book,id=int(bookId))

@app.route('/passwordReset',methods=['GET','POST'])
def passwordReset():
   form=PasswordResetForm()
   if form.validate_on_submit():
     user=User.query.filter_by(email=form.email.data).first()
     msg = Message("Hello",sender="BookSellersUFV@gmail.com",recipients=[user.email],html=render_template('verify.html'))
     mail.send(msg)
     return "Message sent!"        
   return render_template('password.html',form=form)   

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
