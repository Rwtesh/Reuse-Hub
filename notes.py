import pymongo
from main import authentication


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["notes_database"]
collection = db["notes_info"]


def main():
    check = authentication()
    if check == True:
        while True:
            print("\n===== NOTES PORTAL =====")
            print("1. Add Notes (Google Drive link)")
            print("2. Show Notes")
            print("3. Exit")
            choice = input("Enter your choice: ")

            if choice == "1":
                add_notes()
            elif choice == "2":
                show_notes()
            elif choice == "3":
                print("Exiting...")
                break
            else:
                print("Invalid choice! Try again.")

def add_notes():
    print("\n--- Add New Notes ---")
    name = input("Your Name: ").strip()
    sem = input("Semester: ").strip()
    branch = input("Branch: ").strip()
    subject = input("Subject: ").strip()
    chapter = input("Chapter: ").strip()
    drive_link = input("Enter Google Drive link of the PDF only: ").strip()

    if not drive_link.startswith("http://drive"):
        print("Invalid link! Please paste a valid Google Drive link.")
        return

    note_doc = {
        "name": name,
        "semester": sem,
        "branch": branch,
        "subject": subject,
        "chapter": chapter,
        "drive_link": drive_link
    }

    collection.insert_one(note_doc)
    print("Notes link added successfully!")

def show_notes():
    print("\n--- View Notes ---")
    branch = input("Enter Branch: ").strip()
    subject = input("Enter Subject: ").strip()

    notes = collection.find({"branch": branch, "subject": subject})

    found = False
    for note in notes:
        found = True
        print("\n-"*30)
        print(f"Name: {note['name']}")
        print(f"Semester: {note['semester']}")
        print(f"Branch: {note['branch']}")
        print(f"Subject: {note['subject']}")
        print(f"Chapter: {note['chapter']}")
        print(f"Drive Link: {note['drive_link']}")
        print("-"*30)

    if not found:
        print("No notes found for that branch and subject.")


if __name__ == "__main__":
    main()
