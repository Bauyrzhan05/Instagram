from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId

post_likes = Blueprint("post_likes", __name__)

@post_likes.route("/like/<post_id>", methods=["POST"])
@jwt_required()
def like_post(post_id):
    mongo = current_app.mongo
    user_id = ObjectId(get_jwt_identity())

    post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})
    if not post:
        return jsonify({"success": False, "error": "Post not found"}), 404

    if user_id in post.get("likes", []):
        mongo.db.posts.update_one({"_id": ObjectId(post_id)}, {"$pull": {"likes": user_id}})
    else:
        mongo.db.posts.update_one({"_id": ObjectId(post_id)}, {"$addToSet": {"likes": user_id}})

    # ✅ Пост жаңартылғаннан кейін оқып, қайтарамыз
    updated_post = mongo.db.posts.find_one({"_id": ObjectId(post_id)})

    updated_post["_id"] = str(updated_post["_id"])
    updated_post["user_id"] = str(updated_post["user_id"])
    updated_post["likes"] = [str(uid) for uid in updated_post.get("likes", [])]

    return jsonify({"success": True, "data": updated_post}), 200

