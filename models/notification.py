from db import db

class Notification(db.Model):
    __tablename__='notification'

    notification_id=db.Column(db.String(100),primary_key=True)
    message=db.Column(db.String(255))
    title=db.Column(db.String(255),nullable=True)
    ServiceID=db.Column('serviceID',db.String(255),nullable=True)

    type_id=db.Column(db.String(100),db.ForeignKey("notification_type.type_id"),nullable=False)

    sent_notification=db.relationship("Sent_Notification",back_populates="notification")

    notification_type = db.relationship("Notification_type",back_populates="notification")