from app.src.db.init import db

class ActivitySurvey(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    question1 = db.Column(db.String(255))  
    question2 = db.Column(db.Integer)     
    question3 = db.Column(db.String(255)) 
    question4 = db.Column(db.String(255))    
    question5 = db.Column(db.String(255)) 
    question6 = db.Column(db.String(255)) 
    question7 = db.Column(db.String(255)) 
    question8 = db.Column(db.String(255))  
    question9 = db.Column(db.String(255))
    user_dislike = db.Column(db.String(255), nullable=True, default=None)

    user = db.relationship('User', backref=db.backref('ActivitySurvey', lazy=True))