from flask import Flask, request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_babel import Babel
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = '5791628bb0b13ce0c676dfde280ba245'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
admin = Admin()
babel = Babel()
login_manager = LoginManager(app)
login_manager.init_app(app)
admin.init_app(app)
babel.init_app(app)

from app import views, models, db
from app.models import User, Appointment, Doctors, Messages, Blogs, Newsletter, BlogTags, Categories

if not 'User' in locals():
    class User(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(64), index=True, unique=True)
        email = db.Column(db.String(120), index=True, unique=True)
        password_hash = db.Column(db.String(128))

        def __repr__(self):
            return '<User {}>'.format(self.username)

        def set_password(self, password):
            self.password_hash = generate_password_hash(password)

        def check_password(self, password):
            return check_password_hash(self.password_hash, password)
    
admin.add_view(ModelView(User, db.session))

if not 'Doctors' in locals():
    class Doctors(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        username = db.Column(db.String(64), index=True, unique=True)
        department = db.Column(db.String(64), index=True)
        
admin.add_view(ModelView(Doctors, db.session))

if not 'Department' in locals():
    class Department(db.Model):
        __table_args__ = {'extend_existing': True}
        id = db.Column(db.Integer, primary_key=True)
        department = db.Column(db.String(64), index=True)
        
admin.add_view(ModelView(Department, db.session))

if not 'Appointment' in locals():
    class Appointment(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(64), index=True)
        email = db.Column(db.String(120), index=True)
        phone = db.Column(db.String(15), index=True)
        doctor_name = db.Column(db.String(64), index=True)
        date = db.Column(db.Date, index=True)
        message = db.Column(db.String(256), index=True)
        
admin.add_view(ModelView(Appointment, db.session))

if not 'Messages' in locals():
    class Messages(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(64), index=True)
        email = db.Column(db.String(120), index=True)
        phone = db.Column(db.String(15), index=True)
        subject = db.Column(db.String(64), index=True)
        message = db.Column(db.String(512), index = True)
        
admin.add_view(ModelView(Messages, db.session))
        
if not 'BlogPost' in locals():
    class BlogPost(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(64), index=True)
        surname = db.Column(db.String(64), index=True)
        email = db.Column(db.String(120), index=True)
        message = db.Column(db.String(512), index = True)
        
admin.add_view(ModelView(Blogs, db.session))

if not 'Newsletter' in locals():
    class Newsletter(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        email = db.Column(db.String(120), index=True)
        
admin.add_view(ModelView(Newsletter, db.session))

if not 'BlogTags' in locals():
    class BlogTags(db.Model):
        __tablename__ = 'blog_tags'
        id = db.Column(db.Integer, primary_key=True)
        tags = db.Column(db.String(64), index=True)
        
admin.add_view(ModelView(BlogTags, db.session))

if not 'Categories' in locals():
    class Categories(db.Model):
        id = db.Column(db.Integer, primary_key = True)
        categories = db.Column(db.String(64), index=True)
        
admin.add_view(ModelView(Categories, db.session))

@app.route('/_footer', methods=['POST'])
def add_email_to_newsletter():
    if request.method == 'POST':
        email = request.form['email']
        new_email = Newsletter(email=email)
        try:
            db.session.add(new_email)
            db.session.commit()
            flash('Email added to the newsletter successfully!', 'success')
        except:
            db.session.rollback()
            flash('Error adding email to the newsletter!', 'danger')
        finally:
            db.session.close()
            
    return redirect(url_for('index'))

@app.route('/contact', methods=['POST'])
def add_message():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        subject = request.form['subject']
        message = request.form['message']
        new_message = Messages(name=name, email=email, phone=phone, subject=subject, message=message)
        try:
            db.session.add(new_message)
            db.session.commit()
            flash('Message added to the messages successfully!', 'success')
        except:
            db.session.rollback()
            flash('Error adding message to the messages!', 'danger')
        finally:
            db.session.close()
            
    return redirect(url_for('contact'))

@app.route('/appointment', methods=['POST'])
def add_appointment():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']
        doctor_name = request.form['doctor_name']  # Değişiklik burada
        date_str = request.form['date']

        # Tarihi uygun bir Python tarih nesnesine çevir
        try:
            date = datetime.strptime(date_str, '%m/%d/%Y').date()
        except ValueError:
            print("Invalid date format")
            # İsterseniz burada bir hata mesajı dönebilir veya başka bir işlem yapabilirsiniz.
            return redirect(url_for('appointment'))

        message = request.form['message']
        new_appointment = Appointment(name=name, email=email, phone=phone, doctor_name=doctor_name, date=date, message=message)

        try:
            db.session.add(new_appointment)
            db.session.commit()
            flash('Appointment added to the appointments successfully!', 'success')
        except Exception as e:
            print(f"Error: {str(e)}")
            db.session.rollback()
            flash('Error adding appointment to the appointments!', 'danger')
        finally:
            db.session.close()

    return redirect(url_for('appointment'))

@app.route('/blogs', methods=['POST'])
def add_comment():
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        email = request.form['email']
        message = request.form['message']
        new_comment = Blogs(name=name, surname=surname, email=email, message=message)
        try:
            db.session.add(new_comment)
            db.session.commit()
            flash('Comment added to the blogs successfully!', 'success')
        except:
            db.session.rollback()
            flash('Error adding comment to the blogs!', 'danger')
        finally:
            db.session.close()
            
    return redirect(url_for('blogs'))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

