import datetime

class Post:
    def __init__(self, user_id, description, media_url=None):
        self.user_id = user_id
        self.description = description
        self.media_url = media_url
        self.created_at = datetime.datetime.utcnow()

    def to_dict(self):
        return {
            "user_id": self.user_id,
            "description": self.description,
            "media_url": self.media_url,
            "created_at": self.created_at
        }

    @staticmethod
    def remove_post(mongo, post_id):
        mongo.db.posts.delete_one({"_id": ObjectId(post_id)})