from db import db
from sqlalchemy.types import TIMESTAMP
from sqlalchemy.sql import func
class Sent_Notification(db.Model):
    __tablename__="sent_notification"
    sid=db.Column(db.String(100),primary_key=True)
    read_datetime=db.Column( TIMESTAMP(timezone=False), 
        server_default=func.now())
    is_read=db.Column(db.Boolean)
    delivery_status=db.Column(db.String(30))
    sent_at=db.Column(TIMESTAMP(timezone=False),server_default=func.now())
    sent_to=db.Column(db.String(100),nullable=False)
    carriersid=db.Column(db.String(100))
    message_id=db.Column(db.String(100))

    user_id=db.Column(db.String(100),db.ForeignKey("users.user_id"))

    user=db.relationship("User")

    notification_id=db.Column(db.String(100),db.ForeignKey("notification.notification_id"))

    notification=db.relationship("Notification",back_populates="sent_notification")
