from datetime import datetime
from app import db
from .classification import Classification

class URLScrape(db.Model):
    __tablename__ = 'url_scrape'

    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.Text, nullable=False)
    scraped_content = db.Column(db.Text, nullable=True)
    classification_id = db.Column(db.Integer, db.ForeignKey('classification.id'))
    last_scraped = db.Column(db.DateTime, default=datetime.utcnow)

    classification = db.relationship('Classification', backref='scrapes')

    def __repr__(self):
        return f"<URLScrape(id={self.id}, url={self.url})>"
