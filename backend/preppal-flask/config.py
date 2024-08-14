import os
from dotenv import load_dotenv

# Load environmental variables from .env file
load_dotenv()

class Config:
    # Database Url Configurations
    database_name = os.getenv("DATABASE_NAME")
    db_username = os.getenv("DB_USERNAME")
    db_password = os.getenv("DB_PASSWORD")

    db_url = f'postgresql://{db_username}:{db_password}@localhost/{database_name}'

    print(db_url)

    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', db_url)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
