# Message Sender

A utility application that helps you send multiple messages automatically with customizable timing. The program splits messages by newlines and sends them sequentially to any text input field.

## Features

- User-friendly graphical interface
- Send multiple messages automatically
- Customizable delay timer before starting
- Split messages by newlines
- Progress tracking
- Works with any application that accepts text input

## Installation

1. Download the latest release from the [Releases](../../releases) page
2. Extract the zip file
3. Run the MessageSender.exe file

## Usage

1. Launch the MessageSender application
2. Enter your messages in the text area (one message per line)
3. Set the delay time (in seconds) before the program starts sending messages
4. Click "Send Messages"
5. Switch to your target application window during the delay countdown
6. The program will automatically type and send each message

## Requirements

- Windows 10 or later
- Any application that accepts text input (messaging apps, text editors, etc.)

## Building from Source

If you want to build the project from source:

1. Clone the repository
2. Install Python 3.x
3. Install required dependencies:
   ```bash
   pip install pyautogui
   pip install pyinstaller
   ```
4. Build the executable:
   ```bash
   pyinstaller --onefile --noconsole --icon=icon.ico --name MessageSender --clean message_sender_gui.py
   ```

## Technical Details

Built using:
- Python
- tkinter for GUI
- pyautogui for message automation
<<<<<<< HEAD
- Threading for non-blocking operation 
=======
- Threading for non-blocking operation 
>>>>>>> 84e669f15ffc8d3483394ade175d05ea5b26e88b
