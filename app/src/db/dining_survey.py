from app.src.db.init import db

class DiningSurvey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question1 = db.Column(db.String(255))  # Cuisine preference
    question2 = db.Column(db.Integer)      # Travel distance preference
    question3 = db.Column(db.String(255))  # Dietary restrictions
    question4 = db.Column(db.Integer)      # Ambiance importance
    question5 = db.Column(db.String(255))  # Price range
    question6 = db.Column(db.String(255))  # Preferred meal
    question7 = db.Column(db.String(255))  # Fast-casual or full-service
    question8 = db.Column(db.Integer)      # Willingness to try new things
    question9 = db.Column(db.String(255))  # Takeout or delivery preference
    question10 = db.Column(db.Integer)     # Sustainability importance

    user = db.relationship('User', backref=db.backref('DiningSurvey', lazy=True))