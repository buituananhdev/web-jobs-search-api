from api.models.database import db

class Candidate(db.Model):
    __tablename__ = 'Candidates'
    candidate_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey('Accounts.account_id'), nullable=False)
    account = db.relationship('Account', backref=db.backref('candidates', lazy=True))
