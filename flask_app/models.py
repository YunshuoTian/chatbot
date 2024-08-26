from flask_app import db
from flask_login import UserMixin
import uuid


def generate_uuid():
    return str(uuid.uuid4())

class Users(db.Model, UserMixin):
    __tablename__ = 'users'

    uid = db.Column(db.String, default=generate_uuid, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)

    def __repr__(self):
        return f"<uid: {self.uid}, Username: {self.username}>"
    
    def get_id(self):
        return self.uid

class Chats(db.Model):
    __tablename__ = 'chats'
    
    cid = db.Column(db.String,  default=generate_uuid, primary_key=True)
    uid = db.Column(db.String, nullable=False)
    thread_id = db.Column(db.String)
    user_input = db.Column(db.Text)
    bot_input = db.Column(db.Text)

    def __repr__(self):
        return f"<uid: {self.uid}, cid: {self.cid}>"