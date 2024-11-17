from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root@localhost/blogapp'
db = SQLAlchemy(app)


class Contact(db.Model):
   sno = db.Column(db.Integer, primary_key=True)
   name = db.Column(db.String(100), nullable=False)
   email = db.Column(db.String(100), nullable=False)
   message = db.Column(db.Text, nullable=False)



@app.route('/')
def home():
   return render_template('index.html')


@app.route('/post')
def post():
   return render_template('post.html')


@app.route('/about')
def about():
   return render_template('about.html')


@app.route('/contact')
def contact():
   if request.method == 'POST':
       name = request.form.get('name')
       email = request.form.get('email')
       Msg = request.form.get('message')
       entry = Contact(name=name, email=email, message=Msg)
       db.session.add(entry)
       db.session.commit()
   return render_template('contact.html')


@app.route('/login')
def login():
   return render_template('login.html')


if __name__ == '__main__':
   with app.app_context():
       db.create_all()
       app.run(debug=True, port=3306)



