import firebase_admin
from firebase_admin import db, credentials
import os

# Initialize the Firebase app

script_dir = os.path.dirname(os.path.abspath(__file__))
cred_file = os.path.join(script_dir, 'credential.json')
flag_file = os.path.join(script_dir, 'exit_flag')

cred = credentials.Certificate(cred_file)
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://terminal-chat-51395-default-rtdb.asia-southeast1.firebasedatabase.app/"
})

def user_input():
    # Ask for the username
    username = input("Enter your username: ")
    print(f"Welcome, {username}! You can start typing your messages.")

    messages_ref = db.reference("/messages")
    
    while True:
        user_text = input("Enter your message (or type 'exit' to quit): ")
        if user_text.lower() == 'exit':
            print("Exiting...")
            # Create an empty flag file to signal the receiver to exit
            open(flag_file, 'a').close()
            break

        # Push the message to Firebase
        new_msg_ref = messages_ref.push()
        new_msg_ref.set({
            "username": username,
            "message": user_text
        })

if __name__ == "__main__":
    user_input()
