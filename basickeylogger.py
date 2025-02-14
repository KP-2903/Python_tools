import pyperclip
import time
from pynput import keyboard

# List to store clipboard contents
clipboard_list = []

# Function to get key name from the keyboard event
def get_key_name(key):
    if isinstance(key, keyboard.KeyCode):
        return key.char
    else:
        return str(key)

# Function to handle key press events
def on_press(key):
    key_name = get_key_name(key)
    print(f"Key {key_name} pressed")

# Function to handle key release events
def on_release(key):
    key_name = get_key_name(key)
    print(f"Key {key_name} released")
    # Exit the program when 'Esc' is pressed
    if str(key_name) == 'Key.esc':
        print("Exiting program...")
        return False

# Function to monitor clipboard content
def monitor_clipboard():
    print("Starting clipboard monitoring. Press 'Esc' to stop...")
    while True:
        try:
            # Get the current clipboard content
            clipboard_content = pyperclip.paste()
            # Check if content is new and not already in the list
            if clipboard_content and clipboard_content not in clipboard_list:
                clipboard_list.append(clipboard_content)
                print(f"Clipboard updated: {clipboard_list}")
            time.sleep(3)
        except KeyboardInterrupt:
            print("Clipboard monitoring stopped.")
            break

# Start keyboard listener in a separate thread
def main():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        monitor_clipboard()
        listener.join()

if __name__ == "__main__":
    main()
