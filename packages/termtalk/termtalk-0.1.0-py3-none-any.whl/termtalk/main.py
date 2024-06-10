
import platform
import os
import time
from . import sender

# Get the directory of the current script
script_dir = os.path.dirname(os.path.abspath(__file__))
flag_file = os.path.join(script_dir, 'exit_flag')
receiver_path = os.path.join(script_dir, 'receiver.py')

def start_receiver():

    
    if platform.system() == "Windows":
        os.system(f'start cmd /k python {receiver_path}')
    elif platform.system() == "Darwin":  # macOS
        os.system(f'open -a Terminal python {receiver_path}')
    else:  # Assume Unix-like (Linux)
        os.system(f'gnome-terminal -- python3 {receiver_path}')

def user_input():
    while True:
        user_text = input("Enter your message (or type 'exit' to quit): ")
        if user_text.lower() == 'exit':
            print("Exiting...")
            open(flag_file, 'a').close()
            break
        print(f"You entered: {user_text}")

def start():
    # Remove the flag file if it exists
    if os.path.exists(flag_file):
        os.remove(flag_file)

    # Start the receiver in a new terminal
    start_receiver()

    # Give some time for the new terminal to open
    time.sleep(2)

    # Start the sender in the current terminal
    sender.user_input()

if __name__ == "__main__":
    start()


