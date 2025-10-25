import os
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.post import Post
from werkzeug.utils import secure_filename
from bson import ObjectId
from bson.errors import InvalidId

posts = Blueprint("posts", __name__)

UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "mp4"}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@posts.route("/create", methods=["POST"])
@jwt_required()
def create_post():
    user_id = get_jwt_identity()

    description = request.form.get("description")
    file = request.files.get("media")

    media_url = None
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        media_url = f"/uploads/{filename}"

    new_post = Post(user_id=user_id, description=description, media_url=media_url)
    mongo = current_app.mongo
    mongo.db.posts.insert_one(new_post.to_dict())

    return jsonify({"success": True, "msg": "Post created successfully"}), 201

@posts.route('/my-posts', methods=['GET'])
@jwt_required()
def get_my_posts():
    user_id = get_jwt_identity()
    mongo = current_app.mongo
    posts_cursor = mongo.db.posts.find({"user_id": user_id}).sort("_id", -1)  # соңғыларын бірінші
    posts = []

    for post in posts_cursor:
        post['_id'] = str(post['_id'])  # JSON-ға айналдыру үшін
        posts.append(post)

    return jsonify({"success": True, "data": posts}), 200

@posts.route('all', methods=['GET'])
def get_all_posts():
    mongo = current_app.mongo
    posts_cursor = mongo.db.posts.find().sort("_id", -1)
    posts = []

    for post in posts_cursor:
        post['_id'] = str(post['_id'])
        post['user_id'] = str(post['user_id'])

        posts.append(post)

    return jsonify({"success": True, "data": posts}), 200

@posts.route("/get-user/<user_id>", methods=["GET"])
def get_user(user_id):
    try:
        mongo = current_app.mongo
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        if user:
            return jsonify({
                "success": True,
                "data": {
                    '_id': str(user['_id']),
                    "username": user.get("username"),
                    "avatar": user.get("avatar"),
                    "bio": user.get("bio"),
                    "followers": user.get("followers"),
                    "following": user.get("following")
                }
            })
        return jsonify({"success": False, "message": "User not found"}), 404
    except InvalidId:
        return jsonify({"success": False, "message": "Invalid user ID"}), 400

@posts.route('/remove/<_id>', methods=['DELETE'])
@jwt_required()
def remove_post(_id):
    mongo = current_app.mongo
    result = mongo.db.posts.delete_one({"_id": ObjectId(_id)})
    if result.deleted_count == 1:
        return jsonify({"success": True, "message": "Post removed"}), 200
    else:
        return jsonify({"success": False, "message": "Post not found"}), 404




