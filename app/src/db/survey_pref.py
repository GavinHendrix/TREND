from app.src.db.init import db

class SurveyPreference(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    dining_survey = db.Column(db.Boolean, default=False)
    activity_survey = db.Column(db.Boolean, default=False)
    movie_survey = db.Column(db.Boolean, default=False)

    user = db.relationship('User', backref=db.backref('SurveyPreference', lazy=True))