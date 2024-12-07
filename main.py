import json
import math

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
    n=2
    last = math.ceil((len(post_data)/n))
    page = request.args.get('page')

    if (not str(page).isnumeric()):
        page = 1
    page = int(page)
    j=(page-1)*n
    posts = post_data[j:j+n]

    if page==1:
        prev = "#"
        next = "/?page="+str(page+1)
    elif page==last:
        prev = "/?page="+str(page-1)
        next = "#"
    else:
        prev = "/?page="+str(page-1)
        next = "/?page="+str(page+1)

    return render_template('index.html', param=params, posts=post_data, prev=prev, next=next)


@app.route('/post/<slug>', methods=['GET', 'POST'])
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
@app.route('/admin', methods=['GET', 'POST'])
def dashboard():
    posts = Posts.query.filter_by().all()
    contacts = Contact.query.filter_by().all()
    return render_template('admin/index.html', posts=posts, contacts=contacts)
@app.route('/editPosts/<string:post_id>', methods=['GET', 'POST'])
def edit(post_id):
    if request.method == 'POST':
        ntitle = request.form['title']
        nsubtitle = request.form['subTitle']
        if post_id == '0':
            pass
        else:
            post = Posts.query.filter_by(post_id=post_id).first()
            post.title = ntitle
            post.sub_title = nsubtitle
         return redirect(url_for('dashboard'))


    return render_template('admin/editPost.html', param=params, post_id=post_id)
if __name__ == '__main__':
   with app.app_context():
       db.create_all()
       app.run(debug=True)



