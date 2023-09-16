from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, request, redirect, url_for, flash
from flask_migrate import Migrate
from werkzeug.security import check_password_hash, generate_password_hash
#from models import User


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///your_database.db'
db = SQLAlchemy(app)
migrate = Migrate(app, db)
app.secret_key = 'my_secret'
# Define a User model for the database
'''class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
'''

class User(db.Model):
    '''id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)'''
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    __tablename__ = 'user'
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@app.route('/', methods=['GET', 'POST'])
def index():
	return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    # Handle login logic here
    message = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Query the database for the user with the provided username
        user = User.query.filter_by(username=username).first()

        #if user and check_password_hash(user.password, password):
        if user: # and user.password_hash == password:
            # Password matches - user is authenticated
            if check_password_hash(user.password_hash, password) or user.password_hash == password:
            	#flash('Login successful!', 'success')
            	message = 'Login successful!'
            	print("Login Successful!")
            	return redirect(url_for('index'))  # Redirect to the home page or a dashboard

        # Authentication failed - credentials not found
        #flash('Credentials not found. Please check your username and password.', 'error')

        message = 'Credentials not found. Please check your username and password.', 'error'

        print("Creds not found")
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Handle registration logic here
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists in the database
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            flash('Username already exists. Please choose a different one.', 'error')
            print("Username already exists")

        # Create a new user and add it to the database
        #new_user = User(username=username, password=password)
        else:
        	new_user = User(username=username, password_hash=password)
        	new_user.set_password(password)
        	db.session.add(new_user)
        	db.session.commit()
       		flash('Registration successful!', 'success')
       		print("Registered successfully")
        #return render_template('reg_success.html')
    return render_template('register.html')




if __name__ == "__main__":
    app.run(debug=True)
