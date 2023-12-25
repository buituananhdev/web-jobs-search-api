from api.models.database import db

class Account(db.Model):
    __tablename__ = 'Accounts'
    account_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(20), nullable=False)

    def check_password(self, password):
        return self.password == password
