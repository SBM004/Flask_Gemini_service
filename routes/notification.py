from flask import Flask, request, Response, Blueprint,jsonify
from models.notification import  Notification
from models.notification_type_model import  Notification_type
from models.sent_notification_models import  Sent_Notification
from models.remainder_model import  Reminder
from datetime import datetime
import uuid
from db import db
notification_route=Blueprint("notification_route",__name__)

@notification_route.route('/send',methods=['POST'])
def send():
    body=request.get_json()
    type_id=Notification_type.query.filter_by(carrier=body["carrier"],type=body["type"]).first()
    if not type_id:
        return jsonify({"m":"no"})
    notification_id=str(uuid.uuid4())
    notification=Notification(notification_id=notification_id,message=body["message"],title=body["title"],type_id=type_id.type_id)
    db.session.add(notification)
    db.session.commit()

    sid=str(uuid.uuid4())
    sent_notific=Sent_Notification(sid=sid,user_id=body["user_id"],notification_id=notification_id,sent_at=datetime.now(),sent_to=body["sent_to"])
    db.session.add(sent_notific)
    db.session.commit()


    return jsonify({"m":"done"})
@notification_route.route('/reminder',methods=['POST'])
def sendnotific():
    body=request.get_json()
    type_id=Notification_type.query.filter_by(carrier=body["carrier"],type="reminder").first()
    if not type_id:
        return jsonify({"m":"no"})
    reminder_id=str(uuid.uuid4())
    #notification_id=str(uuid.uuid4())
    # notification=Notification(notification_id=notification_id,message=body["message"],title=body["title"],type_id=type_id.type_id)
    # db.session.add(notification)
    # db.session.commit()

    # sid=str(uuid.uuid4())
    # sent_notific=Sent_Notification(sid=sid,user_id=body["user_id"],notification_id=notification_id,sent_at=datetime.now(),sent_to=body["sent_to"])
    # db.session.add(sent_notific)
    # db.session.commit()
    try:
        sed_reminder=Reminder(reminder_id=reminder_id,user_id=body["user_id"],sent_to=body["sent_to"],execute_at=body["execute_at"],message=body["message"],title=body["title"])
        db.session.add(sed_reminder)
        db.session.commit()
    except:
        return jsonify({"m":"done"})

    return jsonify({"m":"done"})


