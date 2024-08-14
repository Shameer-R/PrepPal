from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_user
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager()
login_manager.init_app(app)

# Import the user model
from app.models import User

@login_manager.user_loader
def load_user(user_id):
    # Load the user from user model
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('Home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if user already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user is None:

            # Create new user
            new_user = User(username=username, email=email)
            new_user.set_password(password)

            # Add the user to the database
            db.session.add(new_user)
            db.session.commit()

            flash('Registration successful! Please log in.')
            return redirect(url_for('login'))
        else:
            flash('Username/Email already exists!')
            return redirect(url_for('register'))




    return  render_template('Register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        # Fetch the user data form the database
        user = User.query.filter_by(username=username).first()

        if user is None or not user.check_password(password):
            flash("Invalid username or password!")
            return redirect(url_for('login'))

        # Log the user in
        login_user(user)
        return redirect(url_for('home'))
    return render_template('Login.html')

if __name__ == '__main__':
    app.run(debug=True)
