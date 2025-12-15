from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'secret123'


app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class User(db.Model):
id = db.Column(db.Integer, primary_key=True)
username = db.Column(db.String(100), unique=True)
password = db.Column(db.String(200))


@app.route('/', methods=['GET', 'POST'])
def login():
if request.method == 'POST':
user = User.query.filter_by(username=request.form['username']).first()
if user and check_password_hash(user.password, request.form['password']):
session['user'] = user.username
return redirect('/dashboard')
return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
if request.method == 'POST':
hashed = generate_password_hash(request.form['password'])
user = User(username=request.form['username'], password=hashed)
db.session.add(user)
db.session.commit()
return redirect('/')
return render_template('register.html')


@app.route('/dashboard')
def dashboard():
if 'user' not in session:
return redirect('/')
return render_template('dashboard.html', user=session['user'])


@app.route('/class/<class_name>')
def live_class(class_name):
return render_template('class.html', class_name=class_name)


@app.route('/logout')
def logout():
session.clear()
return redirect('/')


if __name__ == '__main__':
with app.app_context():
db.create_all()
app.run(debug=True)