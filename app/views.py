from flask import render_template, redirect, url_for, request, flash
from app import app, db
from app.forms import LoginForm, RegisterForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Department, Doctors, Blogs, BlogTags, Categories, Appointment

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/temp', methods=['GET', 'POST'])
def temp():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('temp'))
        
        login_user(user, remember=form.remember_me.data)
        
        # Giriş yapan kullanıcının email'ine sahip randevuları çek
        user_appointments = Appointment.query.filter_by(email=user.email).all()
        
        # Randevuları template'e gönder
        return render_template('dashboard.html', title='Dashboard', appointments=user_appointments)
    
    return render_template('temp.html', title='Sign In', form=form)

@app.route('/dashboard')
@login_required
def dashboard():
    # Giriş yapan kullanıcının email'ine sahip randevuları çek
    user_appointments = Appointment.query.filter_by(email=current_user.email).all()
    return render_template('dashboard.html', appointments=user_appointments)

@app.route('/blogs')
def blogs():
    comments = Blogs.query.all()
    tags = BlogTags.query.all()
    categories = Categories.query.all()
    return render_template('blog-single.html', comments=comments, tags=tags, categories=categories)

@app.route('/portfolio')
def portfolio():
    return render_template('portfolio-details.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/learn')
def learn():
    return render_template('learn_more.html')

@app.route('/appointment')
def appointment():
    departments = Department.query.all()
    doctors = Doctors.query.all()
    return render_template('appointment.html', departments=departments, doctors=doctors)
  
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user() 
    return redirect(url_for('index'))
  
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    
    return render_template('register.html', title='Register', form=form)
  


