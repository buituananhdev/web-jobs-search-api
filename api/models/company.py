from api.models.database import db

class Company(db.Model):
    __tablename__ = 'companies'
    company_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    location = db.Column(db.String(40))
    account_id = db.Column(db.Integer, db.ForeignKey('Accounts.account_id'), nullable=False)
    account = db.relationship('Account', backref=db.backref('companies', lazy=True))
    # Thêm quan hệ với Job
    jobs = db.relationship('Job', back_populates='company')
    