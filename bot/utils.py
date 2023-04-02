from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]


def get_user_progress(username):
    user_data = db.users.find_one({"username": username})
    if user_data is None:
        return None
    return user_data.get("progress")
