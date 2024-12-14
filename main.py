import json
import math

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import *
from flask_login import LoginManager, login_user, login_required, current_user, UserMixin
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
    location = db.Column(db.String(100), nullable = True)
    author = db.Column(db.String(100), nullable = True)
    image = db.Column(db.String(100), nullable = True)
    #data_posted = db.Column(db.Date)
    content_1 =  db.Column(db.Text, nullable = True)
    content_2 =  db.Column(db.Text, nullable = True)
    slug = db.Column(db.String(100), unique = True, nullable = True)

class Users(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)


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
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = Users.query.filter_by(username=username).first()
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            print("Invalid username or password")
            return redirect(url_for('login'))
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
        locationname = request.form['location']
        slugn = request.form['slug']
        if post_id == '0':
            post = Posts(title=ntitle, sub_title=nsubtitle)
            db.session.add(post)
            db.session.commit()
        else:
            post = Posts.query.filter_by(post_id=post_id).first()
            post.title = ntitle
            post.sub_title = nsubtitle
            post.location = locationname
            post.slug = slugn
            db.session.commit()
        return redirect(url_for('dashboard'))
    post = Posts.query.filter_by(post_id=post_id).first()

    return render_template('admin/editPost.html', param=params, post_id=post_id, post=post)
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        entry = Users(name=name, email=email, username=username, password=password)
        db.session.add(entry)
        db.session.commit()
    return render_template('signup.html', param=params)
#login manager
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

if __name__ == '__main__':
   with app.app_context():
       db.create_all()
       app.run(debug=True)



