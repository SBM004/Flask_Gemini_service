from flask import Blueprint , Flask, request, jsonify
from db import db
from models.User_models import User
import uuid 
user_route=Blueprint('user_route',__name__)

@user_route.route('/')
def get_all():
    users= User.query.all()
    lists=[{"id":user.user_id,"name":user.name,"email":user.email,"role":user.role} for user in users ]
    return jsonify(lists)

@user_route.route('/register',methods=['POST'])
def register():
    body=request.get_json()
    if not body or "name" not in body.keys() or "email" not in body.keys() or "password" not in body.keys() or "role" not in body.keys() or "phone_number" not in body.keys():
        return jsonify({"message":"the data is incomplete"})
    user=User.query.filter_by(email=body["email"]).first()
    if user:
        return jsonify({"message":"the email is allready present"})
    userid=uuid.uuid4()
    user= User(user_id=userid,name=body["name"],email=body["email"],password=body["password"],role=body["role"],phone_number=body["phone_number"])

    db.session.add(user)
    db.session.commit()
    return jsonify({"message":"done "})


@user_route.route('/update',methods=['PUT'])
def upd():
    body=request.get_json()
    user=User.query.filter_by(user_id=body.get("user_id")).first()
    if not user:
         return  jsonify({"message":"not found "})
    user.name=body["name"]
    user.password=body["password"]
    user.email=body["email"]
    user.password=body["password"]

    db.session.commit()
    return  jsonify({"message":"done "})

