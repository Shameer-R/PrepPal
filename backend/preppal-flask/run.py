from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
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

# Import the user and user preferences model
from app.models import User, UserPreferences

@login_manager.user_loader
def load_user(user_id):
    # Load the user from user model
    return User.query.get(int(user_id))

@app.route('/', methods=['GET', 'POST'])
def home():
    if request.method == "POST":
        if 'logout' in request.form: # If user presses logout button
            logout_user()
            flash("You have been logged out.")
            return redirect(url_for('home'))
        elif 'preferences' in request.form: # If user is submitting preferences
            # Retrieving dropdown selections
            cuisine_dropdown = request.form.get('cuisine')
            likes_dropdown = request.form.get('likes')
            allergies_dropdown = request.form.get('allergies')

            user_preferences = UserPreferences.query.filter_by(user_id=current_user.id).first()

            if user_preferences is None:
                # If user preferences don't exist create a new one
                user_preferences = UserPreferences(user_id=current_user.id)
                db.session.add(user_preferences)

            if cuisine_dropdown:
                user_preferences.add_cuisine(cuisine_dropdown)
                print(cuisine_dropdown + " has been added to cuisine column")

            if allergies_dropdown:
                user_preferences.add_allergies(allergies_dropdown)
                print(allergies_dropdown + " has been added to allergies column")

            if likes_dropdown:
                user_preferences.add_likes(likes_dropdown)
                print(likes_dropdown + " has been added to likes")

            # Commit changes to database
            db.session.commit()

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
