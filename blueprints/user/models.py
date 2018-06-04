from  extensions import db
from flask import session
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(UserMixin,db.Model):
    id=db.Column(db.Integer,index=True,primary_key=True,autoincrement=True)
    name=db.Column(db.String(100))
    email=db.Column(db.String(100),unique=True)
    phone=db.Column(db.String,unique=True,nullable=True)
    password=db.Column(db.String,unique=True)
    image=db.Column(db.String,unique=True,nullable=True)
    role=db.Column(db.Integer,default=0)#0 is viewwer 1 is commedian 2is admin 3 is bkdoor

    def save(self):
        db.create_all()
        db.session.add(self)
        db.session.commit()

    def __init__(self):
        return

    def encrypt_password(self,plaintext_password):

        if plaintext_password:
            self.password = generate_password_hash(plaintext_password)
        return

    def authenticate(self,hash,passw):
        x=check_password_hash(hash, passw)
        return x

    def update(self):
        db.session.commit()

class Token(db.Model):
    id=db.Column(db.Integer,index=True,primary_key=True,autoincrement=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    api_token=db.Column(db.Text,nullable=True)
    created_at=db.Column(db.DateTime)
    expires_at=db.Column(db.DateTime)

    def save(self):
        db.create_all()
        db.session.add(self)
        db.session.commit()

    def set_dates(self):
        from datetime import date, datetime, timedelta
        current_date = datetime.now()
        self.created_at=current_date
        expdate = current_date + timedelta(days=30)
        self.expires_at=expdate

    def update(self):
        db.session.commit()



