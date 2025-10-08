from sign_in import signin 
from sign_up import signup 
def authentication():
    while True:
        print("1. New User")
        print("2. Old User")
        c = int(input("choice: "))
        if c == 1:
            print("NEW ACCOUNT")
            signup()
            continue
        
        if c==2:
            check = signin()
            if check == True:
                return True
        
    
if __name__ == "__main__":
    authentication()







