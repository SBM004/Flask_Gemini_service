from db import db

class Notification_type(db.Model):
    __tablename__='notification_type'


    type_id=db.Column(db.String(100),primary_key=True)
    type=db.Column(db.String(100))
    carrier=db.Column(db.String(100))
    notification=db.relationship("Notification",back_populates="notification_type",cascade="all, delete")

  