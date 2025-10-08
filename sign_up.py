import pymongo
import keyboard
import re
def signup():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["authentication"]
    connection = db["users"]
    

    while True:
        user_name = input("USER NAME:\n(Press 1 to go back) ")
        if user_name == "1":
            return False
        if user_name == "exit": return False
        pattern = r'^\d+@geu\.ac\.in$'
        if not re.match(pattern, user_name):
            print("Invalid ID")
        else:
            exist = connection.find_one({"user_name" : user_name})
            if exist:
                print("Account Already existed")
            else: break

    while True:
        user_password = input("Password: \n(Press 1 to go back) ")
        if user_password == "1":
            return False
        if user_password == "exit": return False
        if user_password.isspace():
            print("Password cannot be empty or spaces only")
            continue

        if not any(c.islower() for c in user_password):
            print("Password must have at least one lowercase letter")
            continue

        if not any(c.isupper() for c in user_password):
            print("Password must have at least one uppercase letter")
            continue

        if not any(c.isdigit() for c in user_password):
            print("Password must have at least one number")
            continue

        break

    connection.insert_one({"user_name": user_name, "password": user_password})

    return True

if __name__ == "__main__":
    signup()
