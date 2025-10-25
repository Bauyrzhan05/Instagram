from werkzeug.security import generate_password_hash, check_password_hash

class User:
    def __init__(self, username, email, password, role="user"):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.role = role

    def to_dict(self):
        return {
            "username": self.username,
            "email": self.email,
            "password_hash": self.password_hash,
            "role": self.role
        }

    @staticmethod
    def check_password(password_hash, password):
        return check_password_hash(password_hash, password)
