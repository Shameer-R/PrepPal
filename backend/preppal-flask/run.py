from flask import Flask, render_template
from flask_login import LoginManager, current_user
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
    return  render_template('Register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('Login.html')

if __name__ == '__main__':
    app.run(debug=True)
