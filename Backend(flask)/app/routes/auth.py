from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from models.user import User
from bson import ObjectId, regex
import re

auth = Blueprint("auth", __name__)

@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("name")
    email = data.get("email")
    password = data.get("password")

    mongo = current_app.mongo
    existing_user = mongo.db.users.find_one({"email": email})

    if existing_user:
        return jsonify({"success": False, "msg": "User already registered"}), 400

    new_user = User(username, email, password)
    mongo.db.users.insert_one(new_user.to_dict())

    return jsonify({"success": True, "msg": "User registered successfully"}), 201


@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    mongo = current_app.mongo
    user = mongo.db.users.find_one({"email": email})

    if not user or not User.check_password(user["password_hash"], password):
        return jsonify({"success": False ,"msg": "Invalid email or password"}), 401


    # Тек user_id identity ретінде, ал email мен role — claims
    access_token = create_access_token(identity=str(user['_id']))
    return jsonify({"success": True, "token": access_token}), 200

@auth.route("/search", methods=["GET"])
def search_users():
    mongo = current_app.mongo
    query = request.args.get("name", "").strip()

    if not query:
        return jsonify({"success": False, "error": "Query required"}), 400

    # Іздеу – username ішінде сұрау бар ма
    regex_query = re.compile(f".*{re.escape(query)}.*", re.IGNORECASE)
    users = mongo.db.users.find({"username": {"$regex": regex_query}})

    result = [{
        "_id": str(user["_id"]),
        "username": user.get("username"),
        "avatar": user.get("avatar")
    } for user in users]

    return jsonify({"success": True, "results": result}), 200

@auth.route("/users", methods=["GET"])
def get_all_users():
    mongo = current_app.mongo
    users = mongo.db.users.find()

    result = [{
        "_id": str(user["_id"]),
        "username": user.get("username"),
        "email": user.get("email"),
        "password_hash": user.get("password_hash"),
        "role": user.get("role", "user")
    } for user in users]

    return jsonify({"success": True, "users": result}), 200




