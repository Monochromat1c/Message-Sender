import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import pyautogui
import time
import threading
import sys

class MessageSenderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Message Sender")
        self.root.geometry("500x600")
        
        # Create main frame with padding
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Message input area with emoji support
        ttk.Label(self.main_frame, text="Enter messages (one per line):").grid(row=0, column=0, sticky=tk.W)
        
        # Use Segoe UI Emoji font for Windows or system default emoji font
        emoji_font = ('Segoe UI Emoji', 10) if 'win' in sys.platform else None
        self.message_area = scrolledtext.ScrolledText(
            self.main_frame, 
            width=50, 
            height=20, 
            font=emoji_font
        )
        self.message_area.grid(row=1, column=0, columnspan=2, pady=5)
        
        # Enable proper text wrapping
        self.message_area.configure(wrap=tk.WORD)
        
        # Delay settings
        ttk.Label(self.main_frame, text="Delay before starting (seconds):").grid(row=2, column=0, sticky=tk.W, pady=(10,0))
        self.delay_var = tk.StringVar(value="5")
        self.delay_entry = ttk.Entry(self.main_frame, textvariable=self.delay_var, width=10)
        self.delay_entry.grid(row=2, column=1, sticky=tk.W, pady=(10,0))
        
        # Status label
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(self.main_frame, textvariable=self.status_var)
        self.status_label.grid(row=3, column=0, columnspan=2, pady=5)
        
        # Send button
        self.send_button = ttk.Button(self.main_frame, text="Send Messages", command=self.start_sending)
        self.send_button.grid(row=4, column=0, columnspan=2, pady=5)
        
        # Stop button (disabled by default)
        self.stop_button = ttk.Button(self.main_frame, text="Stop", command=self.stop_sending, state='disabled')
        self.stop_button.grid(row=5, column=0, columnspan=2, pady=5)
        
        self.is_sending = False
        
        # Configure pyautogui
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.001

    def start_sending(self):
        messages = self.message_area.get('1.0', tk.END).splitlines()
        if not messages or all(msg.strip() == '' for msg in messages):
            messagebox.showwarning("Warning", "No messages to send!")
            return
            
        try:
            delay = float(self.delay_var.get())
            if delay < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid delay time!")
            return
            
        self.is_sending = True
        self.send_button.state(['disabled'])
        self.stop_button.state(['!disabled'])
        
        # Start sending in a separate thread
        self.send_thread = threading.Thread(target=self.send_messages, args=(messages, delay))
        self.send_thread.start()
    
    def stop_sending(self):
        self.is_sending = False
        self.status_var.set("Stopped by user")
        self.send_button.state(['!disabled'])
        self.stop_button.state(['disabled'])
    
    def send_messages(self, messages, delay):
        self.status_var.set(f"Starting in {delay} seconds... Focus your target window!")
        time.sleep(delay)
        
        if not self.is_sending:
            return
            
        self.status_var.set("Sending messages...")
        
        try:
            for i, message in enumerate(messages, 1):
                if not self.is_sending:
                    break
                    
                # Send the entire message at once instead of character by character
                # This handles emojis better
                pyautogui.write(message)
                pyautogui.press('enter')
                time.sleep(0.1)  # Slightly longer delay between messages for reliability
                self.status_var.set(f"Sent {i}/{len(messages)} messages")
            
            if self.is_sending:
                self.status_var.set("All messages sent successfully!")
        except Exception as e:
            self.status_var.set(f"Error: {str(e)}")
        finally:
            self.is_sending = False
            self.send_button.state(['!disabled'])
            self.stop_button.state(['disabled'])

def main():
    root = tk.Tk()
    app = MessageSenderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 