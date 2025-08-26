from db import db

class User(db.Model):
    __tablename__="users"

    user_id=db.Column(db.String(100),primary_key=True)
    name= db.Column(db.String(20),nullable=False)
    # name= db.Column(db.String(20),nullable=False)
    email= db.Column(db.String(255),nullable=False)
    role= db.Column(db.String(100),nullable=False)
    password= db.Column(db.String(255),nullable=False)
    phone_number= db.Column(db.String(255),nullable=False)
    # user=db.relationship("User",back_populates="sent_notification")



