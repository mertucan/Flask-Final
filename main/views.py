from flask import render_template
from flask import Blueprint
main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')