import os
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_pymongo import PyMongo
from flask_cors import CORS
from flask import send_from_directory

# Импорттар
from routes.auth import auth
from routes.post import posts
from routes.post_likes import post_likes
from routes.comments import comments
from routes.follow import follow_bp
from routes.story import story_bp
from routes.profile import profile

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

# Конфигурациялар
app.config["MONGO_URI"] = "mongodb+srv://bauyrzhan:erman2023@cluster0.cdvoh.mongodb.net/Instagram"
app.config["JWT_SECRET_KEY"] = 'erman2023secure'
app.config["UPLOAD_FOLDER"] = os.path.join("uploads")

@app.route("/uploads/<path:filename>")
def serve_file(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

jwt = JWTManager(app)
mongo = PyMongo(app)
app.mongo = mongo

app.register_blueprint(auth, url_prefix="/api/auth")
app.register_blueprint(posts, url_prefix="/api/posts")
app.register_blueprint(post_likes, url_prefix="/api/post-likes")
app.register_blueprint(comments, url_prefix="/api/comments")
app.register_blueprint(follow_bp, url_prefix="/api/follows")
app.register_blueprint(story_bp, url_prefix="/api/stories")
app.register_blueprint(profile, url_prefix="/api/profile")

if __name__ == "__main__":
    app.run(debug=True)
