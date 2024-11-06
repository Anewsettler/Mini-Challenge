import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://username:password@localhost:5432/your_database_name'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
