import firebase_admin
from firebase_admin import db, credentials
import os
import platform
from colorama import Fore

#import credential hehe
script_dir = os.path.dirname(os.path.abspath(__file__))
flag_file = os.path.join(script_dir, 'exit_flag')
cred_file = os.path.join(script_dir, 'credential.json')

def is_single_message(data):
    # Check if the first value in the dictionary is a dictionary itself
    if isinstance(data, dict):
        first_value = next(iter(data.values()))
        return not isinstance(first_value, dict)
    return False


def receive_message():
    # Initialize the Firebase app
    cred = credentials.Certificate(cred_file)
    firebase_admin.initialize_app(cred, {
        "databaseURL": "https://terminal-chat-51395-default-rtdb.asia-southeast1.firebasedatabase.app/"
    })

    messages_ref = db.reference("/messages")

    existing_messages = {}

    # def initial_messages_callback(event):
    #     nonlocal existing_messages
    #     existing_messages = event.data if event.data else {}

    # messages_ref.get(initial_messages_callback)

    def message_callback(event):
        new_message = event.data
        if isinstance(new_message, dict):
            if is_single_message(new_message):
                print(f"{Fore.CYAN}{new_message['username']}: {Fore.GREEN}{new_message['message']}")

    messages_ref.listen(message_callback)

    while True:
        if os.path.exists(flag_file):
            break
        else:
            pass


    if platform.system() == "Windows":
        os.system("taskkill /F /IM cmd.exe")
    elif platform.system() == "Darwin":  # macOS
        os.system("osascript -e 'tell application \"Terminal\" to close first window' & exit")
    else:  # Unix-like (Linux)
        os.system("kill -9 $PPID")

if __name__ == "__main__":
    receive_message()


