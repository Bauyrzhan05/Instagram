from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)

# MongoDB конфигурациясы
app.config["MONGO_URI"] = "mongodb+srv://bauyrzhan:erman2023@cluster0.cdvoh.mongodb.net/Instagram"
mongo = PyMongo(app)

# Базаны тексеру
if mongo.db is not None:
    print("connected MongoDB...")
