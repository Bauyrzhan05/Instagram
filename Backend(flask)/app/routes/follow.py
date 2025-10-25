from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId

follow_bp = Blueprint("follow_bp", __name__)

@follow_bp.route("/follow/<user_id>", methods=["POST"])
@jwt_required()
def follow_user(user_id):
    mongo = current_app.mongo
    current_user_id = ObjectId(get_jwt_identity())
    target_user_id = ObjectId(user_id)

    if current_user_id == target_user_id:
        return jsonify({"success": False, "error": "You cannot follow yourself"}), 400

    mongo.db.users.update_one(
        {"_id": current_user_id}, {"$addToSet": {"following": target_user_id}}
    )
    mongo.db.users.update_one(
        {"_id": target_user_id}, {"$addToSet": {"followers": current_user_id}}
    )

    return jsonify({"success": True, "message": "Followed"}), 200

@follow_bp.route("/unfollow/<user_id>", methods=["POST"])
@jwt_required()
def unfollow_user(user_id):
    mongo = current_app.mongo
    current_user_id = ObjectId(get_jwt_identity())
    target_user_id = ObjectId(user_id)

    mongo.db.users.update_one(
        {"_id": current_user_id}, {"$pull": {"following": target_user_id}}
    )
    mongo.db.users.update_one(
        {"_id": target_user_id}, {"$pull": {"followers": current_user_id}}
    )

    return jsonify({"success": True, "message": "Unfollowed"}), 200

@follow_bp.route("/recommendations", methods=["GET"])
@jwt_required()
def get_recommendations():
    mongo = current_app.mongo
    current_user_id = ObjectId(get_jwt_identity())

    current_user = mongo.db.users.find_one({"_id": current_user_id})

    following = current_user.get("following", [])
    following.append(current_user_id)

    recommendations = mongo.db.users.find({
        "_id": {"$nin": following}
    }, {"username": 1, "avatar": 1})

    users = [{"_id": str(user["_id"]),
              "username": user.get("username"),
              "avatar": user.get("avatar") }
             for user in recommendations]

    return jsonify({"success": True, "recommendations": users}), 200
