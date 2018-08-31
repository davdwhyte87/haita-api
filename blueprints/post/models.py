from  extensions import db
import datetime

class Post(db.Model):
    id=db.Column(db.Integer,index=True,primary_key=True,autoincrement=True)
    user_id=db.Column(db.Integer,db.ForeignKey('user.id'),nullable=False)
    text=db.Column(db.Text,nullable=False)
    title=db.Column(db.String, nullable=False)
    image=db.Column(db.Text,nullable=True)
    user= db.relationship('User',lazy=True,backref='post')
    comment=db.relationship('Comment',lazy=True,backref='post',uselist=True)
    likes=db.relationship('Like',lazy=True,backref='post',uselist=True)
    created_at=db.Column(db.DateTime,default=datetime.datetime.now())

    def save(self):
        db.create_all()
        db.session.add(self)
        db.session.commit()

    def get_likes(self):
        self.ulikes=[int(x) for x in self._ulikes.split(';')]

    def __init__(self):
        self._ulikes="0;1;1;3;4;9;0;3;9;9"
        self.get_likes()
        return

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class Comment(db.Model):
    id = db.Column(db.Integer, index=True, primary_key=True, autoincrement=True)
    text = db.Column(db.Text, nullable=False)
    post_id=db.Column(db.Integer,db.ForeignKey('post.id'),nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', lazy=True, backref='comment')

    def save(self):
        db.create_all()
        db.session.add(self)
        db.session.commit()

class Like(db.Model):
    id= db.Column(db.Integer, index=True, primary_key=True, autoincrement=True)
    post_id= db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)
    user_id=db.Column(db.Integer)
    def save(self):
        db.create_all()
        db.session.add(self)
        db.session.commit()
    def delete(self):
            db.session.delete(self)
            db.session.commit()