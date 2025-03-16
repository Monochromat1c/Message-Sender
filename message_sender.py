import pyautogui
import time

def send_messages():
    # List to store all messages
    messages = []
    
    # First phase: Collect all messages
    print("Enter your messages (type 'stop' when finished):")
    while True:
        # Use input() with no strip() to preserve empty lines
        message = input()
        if message.lower() == 'stop':
            break
        # Add the message as-is, even if it's empty
        messages.append(message)
    
    if not messages:
        print("No messages to send. Program terminated.")
        return
        
    # Show summary and prepare for sending
    print(f"\nCollected {len(messages)} messages.")
    print("You have 5 seconds to focus the window where you want to type...")
    time.sleep(5)
    
    # Second phase: Send all messages
    print("Starting to send messages...")
    time.sleep(1)
    
    # Send each message with delay
    for message in messages:
        # Type character by character for reliability
        for char in message:
            pyautogui.write(char)
            time.sleep(0.01)  # Small delay between characters
        pyautogui.press('enter')
        time.sleep(0.0001)  # 0.1ms delay between messages
    
    print("All messages sent!")

if __name__ == "__main__":
    pyautogui.FAILSAFE = True
    # Set up pyautogui to be more reliable
    pyautogui.PAUSE = 0.001
    print("Program started! Move mouse to upper-left corner for emergency stop.")
    send_messages() 