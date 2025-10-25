from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from bson import ObjectId
from werkzeug.utils import secure_filename
import os

profile = Blueprint("profile", __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@profile.route("/update", methods=["PUT"])
@jwt_required()
def update_profile():
    mongo = current_app.mongo
    user_id = get_jwt_identity()

    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    bio = request.form.get("bio", "")
    avatar_url = user.get("avatar", "")

    if 'avatar' in request.files:
        file = request.files['avatar']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            upload_folder = current_app.config.get('UPLOAD_FOLDER', 'uploads')
            os.makedirs(upload_folder, exist_ok=True)

            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)

            # ✅ Тек сыртқы URL-ді сақтаймыз
            avatar_url = f"/uploads/{filename}"

    mongo.db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {
            "bio": bio,
            "avatar": avatar_url
        }}
    )

    return jsonify({
        "success": True,
        "message": "Profile updated successfully",
        "data": {
            "bio": bio,
            "avatar": avatar_url
        }
    }), 200


@profile.route("/me", methods=["GET"])
@jwt_required()
def get_profile():
    mongo = current_app.mongo
    user_id = get_jwt_identity()

    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    user_data = {
        "_id": str(user["_id"]),
        "username": user.get("username", ""),
        "email": user.get("email", ""),
        "bio": user.get("bio", ""),
        "avatar": user.get("avatar", ""),
        "followers": len(user.get("followers", [])),
        "following": [str(uid) for uid in user.get("following", [])]
    }

    return jsonify({"success": True, "data": user_data}), 200
