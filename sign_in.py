import pymongo
import re
def signin():
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["authentication"]
    connection = db["users"]
    
    while True:
        user_name = input("USER NAME: ")
        if user_name == "exit": return False
        pattern = r'^\d+@geu\.ac\.in$'
        if not re.match(pattern, user_name) or not connection.find_one({"user_name" : user_name}):
            print("Invalid ID")
        else:
            while True:
                user_password = input("PASSWORD: ")
                if not connection.find_one({"user_name":  user_name, "password": user_password }):
                    print("Wrong Password")
                    print("press 1 to reset password")
                    print("press 0 to continue")
                    c = int (input("enter choice: "))
                    if c== 1:
                        while True:
                            new_password = input("New Password: ")
                            if new_password == "exit": return False
                            if new_password.isspace():
                                print("Password cannot be empty or spaces only")
                                continue
                            
                            if not any(c.islower() for c in new_password):
                                print("Password must have at least one lowercase letter")
                                continue
                            
                            if not any(c.isupper() for c in new_password):
                                print("Password must have at least one uppercase letter")
                                continue
                            
                            if not any(c.isdigit() for c in new_password):
                                print("Password must have at least one number")
                                continue
                            
                            break
                        connection.update_one(
                            {"user_name": user_name},   
                            {"$set": {"password": new_password}}
                        )
                else: return True

if __name__ == "__main__":
    signin()
    