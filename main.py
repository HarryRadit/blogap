import json

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import *
app = Flask(__name__)

with open("config.json", "r") as c:
    params = json.load(c)["parameters"]

if params['local_server']:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['prod_uri']

SECRET_KEY = params['secret_key']
app.config['SECRET_KEY']
db = SQLAlchemy(app)



class Contact(db.Model):
   sno = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(100), nullable=False)
   email = db.Column(db.String(100), nullable=False)
   message = db.Column(db.Text, nullable=False)
   date = db.Column(db.String(20), nullable = True)

class Posts(db.Model):
    post_id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    sub_title = db.Column(db.String(100))
    location = db.Column(db.String(100))
    author = db.Column(db.String(100))
    image = db.Column(db.String(100))
    #data_posted = db.Column(db.Date)
    content_1 =  db.Column(db.Text)
    content_2 =  db.Column(db.Text)
    slug = db.Column(db.String(100), unique = True)



@app.route('/', methods=['GET', 'POST'])
def home():
    db.session.commit()
    post_data = Posts.query.all()
    return render_template('index.html', param=params, posts=post_data)


@app.route('/post/', methods=['GET', 'POST'])
def post(slug):
   single_post= Posts.query.filter_by(slug=slug).first()
   return render_template('post.html', param=params, post = single_post)


@app.route('/about')
def about():
   return render_template('about.html', param=params)


@app.route('/contact', methods=['GET', 'POST'])
def contact():
   if request.method == 'POST':
       name = request.form.get('name')
       email = request.form.get('email')
       Msg = request.form.get('message')
       entry = Contact(name=name, email=email, message=Msg, date = datetime.today().date())
       db.session.add(entry)
       db.session.commit()
   return render_template('contact.html', param=params)


@app.route('/login')
def login():
   return render_template('login.html', param=params)


if __name__ == '__main__':
   with app.app_context():
       db.create_all()
       app.run(debug=True)



