from app import db
from .classification import Classification

class User(db.Model):
    __tablename__ = 'users'

    user_id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String(100), nullable=False)
    classification_id = db.Column(db.Integer, db.ForeignKey('classification.id'))

    classification = db.relationship('Classification', backref='users')

    def __repr__(self):
        return f"<User(user_id={self.user_id}, user_name={self.user_name})>"
