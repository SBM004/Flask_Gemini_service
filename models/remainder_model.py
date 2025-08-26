from db import db
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
import uuid

class Reminder(db.Model):
    __tablename__ = "reminders"

    reminder_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), nullable=False)
    sent_to = db.Column(db.Text, nullable=False)
    title = db.Column(db.Text, nullable=True)
    message = db.Column(db.Text, nullable=True)
    execute_at = db.Column(db.DateTime(timezone=True), nullable=False)
    timezone = db.Column(db.Text, default="UTC")
    type = db.Column(db.Text, default="reminder")
    carrier = db.Column(db.Text, nullable=True)
    status = db.Column(db.Text, default="scheduled")
    kafka_sid = db.Column(UUID(as_uuid=True), nullable=True)

    queued_at = db.Column(db.DateTime(timezone=True), nullable=True)
    sent_at = db.Column(db.DateTime(timezone=True), nullable=True)
    failed_reason = db.Column(db.Text, nullable=True)
    failed_at = db.Column(db.DateTime(timezone=True), nullable=True)
    cancelled_at = db.Column(db.DateTime(timezone=True), nullable=True)

    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Reminder {self.reminder_id} - {self.status}>"