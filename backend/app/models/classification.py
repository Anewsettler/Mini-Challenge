from app import db

class Classification(db.Model):
    __tablename__ = 'classification'

    id = db.Column(db.Integer, primary_key=True)
    classification = db.Column(db.String(100), nullable=False)
    parent_id = db.Column(db.Integer, db.ForeignKey('classification.id'), nullable=True)
    description = db.Column(db.Text, nullable=True)

    subcategories = db.relationship('Classification', backref=db.backref('parent', remote_side=[id]))

    def __repr__(self):
        return f"<Classification(id={self.id}, classification={self.classification})>"
