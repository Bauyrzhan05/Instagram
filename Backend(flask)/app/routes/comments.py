from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId

comments = Blueprint("comments", __name__)

@comments.route("/comment/<post_id>", methods=["POST"])
@jwt_required()
def add_comment(post_id):
    mongo = current_app.mongo
    user_id = ObjectId(get_jwt_identity())
    data = request.get_json()
    text = data.get("text")
    parent_id = data.get("parent_id")

    comment = {
        "post_id": ObjectId(post_id),
        "user_id": user_id,
        "text": text,
        "parent_id": ObjectId(parent_id) if parent_id else None,
        "replies": []
    }
    result = mongo.db.comments.insert_one(comment)

    # If it's a reply, link it to parent
    if parent_id:
        mongo.db.comments.update_one(
            {"_id": ObjectId(parent_id)},
            {"$push": {"replies": result.inserted_id}}
        )

    return jsonify({"success": True, "message": "Comment added"}), 201

@comments.route("/<post_id>", methods=["GET"])
def get_comments(post_id):
    mongo = current_app.mongo

    try:
        # Коментарийлерді пост ID бойынша табамыз
        comments = list(mongo.db.comments.find({"post_id": ObjectId(post_id)}))

        for comment in comments:
            # MongoDB ObjectId-ларды string-ке айналдыру
            comment["_id"] = str(comment["_id"])
            comment["post_id"] = str(comment["post_id"])
            comment["user_id"] = str(comment["user_id"])
            comment["parent_id"] = str(comment["parent_id"]) if comment["parent_id"] else None
            comment["replies"] = [str(reply_id) for reply_id in comment["replies"]]

        return jsonify({"success": True, "data": comments}), 200

    except Exception as e:
        return jsonify({"success": False, "message": "Қате орын алды", "error": str(e)}), 500

# user can delete himself comment...
