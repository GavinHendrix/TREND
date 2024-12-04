from sqlalchemy import Null
from app.src.db.init import db

class MovieSurvey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question1 = db.Column(db.String(255))
    question2 = db.Column(db.String(255))
    question3 = db.Column(db.String(255))
    question4 = db.Column(db.String(255))

    user = db.relationship('User', backref=db.backref('MovieSurvey', lazy=True))