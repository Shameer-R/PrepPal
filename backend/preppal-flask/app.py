from flask import Flask, render_template
from flask_login import LoginManager, current_user

app = Flask(__name__)

login_manager = LoginManager()
login_manager.init_app(app)

@login_manager.user_loader
def load_user(user_id):
    # Load the user from user model
    pass

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
    app.run()
