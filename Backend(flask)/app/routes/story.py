import os
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from werkzeug.utils import secure_filename
from datetime import datetime, timedelta

story_bp = Blueprint("story_bp", __name__)

# 🧠 TTL индексін 1 рет орнату (expires_at негізінде)
@story_bp.before_app_request
def create_ttl_index():
    mongo = current_app.mongo
    mongo.db.stories.create_index("expires_at", expireAfterSeconds=0)

# ✅ Story жүктеу (24 сағаттан кейін автоматты жойылады)
@story_bp.route("/create", methods=["POST"])
@jwt_required()
def upload_story():
    mongo = current_app.mongo
    user_id = ObjectId(get_jwt_identity())

    if "media" not in request.files:
        return jsonify({"success": False, "error": "No media file provided"}), 400

    file = request.files["media"]
    filename = secure_filename(file.filename)
    filepath = os.path.join("uploads", filename)
    file.save(filepath)

    now = datetime.utcnow()
    story = {
        "user_id": user_id,
        "media_url": filepath,
        "timestamp": now,
        "expires_at": now + timedelta(hours=24)
    }

    mongo.db.stories.insert_one(story)
    return jsonify({"success": True, "message": "Story uploaded"}), 201

# 📥 Белсенді (24 сағат ішінде) Stories алу
@story_bp.route("/story", methods=["GET"])
@jwt_required()
def get_stories():
    mongo = current_app.mongo
    now = datetime.utcnow()

    stories = mongo.db.stories.find({"expires_at": {"$gt": now}})
    data = [{
        "_id": str(s["_id"]),
        "media_url": s["media_url"],
        "user_id": str(s["user_id"]),
        "timestamp": s["timestamp"].isoformat(),
        "views": [str(v) for v in s.get("views", [])]
    } for s in stories]

    return jsonify({"success": True, "stories": data}), 200

# ❌ Story-ді қолданушы өзі өшіреді
@story_bp.route("/delete/<story_id>", methods=["DELETE"])
@jwt_required()
def delete_story(story_id):
    mongo = current_app.mongo
    user_id = ObjectId(get_jwt_identity())

    try:
        story_obj_id = ObjectId(story_id)
    except:
        return jsonify({"success": False, "error": "Invalid story ID"}), 400

    story = mongo.db.stories.find_one({"_id": story_obj_id})
    if not story:
        return jsonify({"success": False, "error": "Story not found"}), 404

    if story["user_id"] != user_id:
        return jsonify({"success": False, "error": "Not authorized to delete this story"}), 403

    mongo.db.stories.delete_one({"_id": story_obj_id})
    return jsonify({"success": True, "message": "Story deleted"}), 200

# other users can see other's story
@story_bp.route("/story/<story_id>", methods=["GET"])
@jwt_required()
def view_story(story_id):
    mongo = current_app.mongo
    user_id = ObjectId(get_jwt_identity())

    try:
        story_obj_id = ObjectId(story_id)
    except:
        return jsonify({"success": False, "error": "Invalid story ID"}), 400

    story = mongo.db.stories.find_one({"_id": story_obj_id})
    if not story:
        return jsonify({"success": False, "error": "Story not found"}), 404

    # Тек expire болмағандарды көруге болады
    if story["expires_at"] < datetime.utcnow():
        return jsonify({"success": False, "error": "Story expired"}), 410

    # Өзі көрмесе, views-қа қосамыз
    if user_id != story["user_id"] and user_id not in story.get("views", []):
        mongo.db.stories.update_one(
            {"_id": story_obj_id},
            {"$addToSet": {"views": user_id}}
        )

    return jsonify({
        "success": True,
        "story": {
            "_id": str(story["_id"]),
            "media_url": story["media_url"],
            "user_id": str(story["user_id"]),
            "timestamp": story["timestamp"].isoformat()
        }
    }), 200

# story's owner can see who saw his stories
@story_bp.route("/story/<story_id>/views", methods=["GET"])
@jwt_required()
def get_story_views(story_id):
    mongo = current_app.mongo
    user_id = ObjectId(get_jwt_identity())

    try:
        story_obj_id = ObjectId(story_id)
    except:
        return jsonify({"success": False, "error": "Invalid story ID"}), 400

    story = mongo.db.stories.find_one({"_id": story_obj_id})
    if not story:
        return jsonify({"success": False, "error": "Story not found"}), 404

    if story["user_id"] != user_id:
        return jsonify({"success": False, "error": "Not authorized to view views"}), 403

    viewer_ids = story.get("views", [])
    viewers = mongo.db.users.find({"_id": {"$in": viewer_ids}})

    data = [{
        "_id": str(user["_id"]),
        "username": user.get("username"),
        "avatar": user.get("avatar")
    } for user in viewers]

    return jsonify({"success": True, "viewers": data}), 200


