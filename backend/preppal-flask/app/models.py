from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

from run import db

class User(db.Model, UserMixin):

    __tablename__ = 'user'  # Explicitly defining the table name

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class UserPreferences(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    cuisine = db.Column(db.String(100))
    dislikes = db.Column(db.String(200))
    allergies = db.Column(db.String(200))

    user = db.relationship('User', backref='user')

    def add_cuisine(self, cuisineString):
        if self.cuisine: # If cuisine column exists
            cuisines = self.cuisine.split(',')
            # Making sure there are no duplicate cuisine
            if cuisineString not in cuisines:
                # Adding new cuisine to list and converting it back into one string
                cuisines.append(cuisineString)
                self.cuisine = ",".join(cuisines)
        else: # If cuisine column doesn't exist
            self.cuisine = cuisineString
