from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")

client["reuse_hub"]["messages"].drop()
client["authentication"]["items"].drop()

print("Dropped reuse_hub.messages and authentication.items collections.")
