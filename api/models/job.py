from api.models.database import db

class Job(db.Model):
    __tablename__ = 'jobs'
    job_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    requirements = db.Column(db.Text)
    salary = db.Column(db.DECIMAL(10, 2))
    location = db.Column(db.String(100))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'), nullable=False)
    
    # Thêm quan hệ với Company
    company = db.relationship('Company', back_populates='jobs')
    