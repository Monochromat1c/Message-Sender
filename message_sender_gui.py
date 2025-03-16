import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import pyautogui
import time
import threading
import sys

class MessageSenderGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Message Splitter & Sender")
        self.root.geometry("500x300")  # Adjusted initial size

        # Use a more modern theme
        style = ttk.Style(self.root)
        style.theme_use('alt')  # 'clam', 'alt', 'default', 'classic' are other options
        
        # Attempting Neumorphism
        style.configure('TFrame', background='#f0f0f0')  # Main background color
        style.configure('TLabel', foreground='black', background='#f0f0f0', font=('Segoe UI', 11))
        style.configure('TEntry', foreground='black', fieldbackground='white', font=('Segoe UI', 11), borderwidth=2, relief="groove")
        style.configure('TScrolledText', foreground='black', fieldbackground='white', font=('Segoe UI', 11), borderwidth=2, relief="groove")

        # Create main frame with padding
        self.main_frame = ttk.Frame(root, padding="20", style='TFrame')
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Make columns and rows expandable
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        self.main_frame.columnconfigure(0, weight=1)

        # Message input area with emoji support
        ttk.Label(self.main_frame, text="Enter messages (one message per line):", font=('Segoe UI', 10)).grid(row=0, column=0, sticky=tk.W, pady=(0, 5))

        # Use Segoe UI Emoji font for Windows or system default emoji font
        emoji_font = ('Segoe UI Emoji', 10) if 'win' in sys.platform else None
        self.message_area = scrolledtext.ScrolledText(
            self.main_frame,
            width=40,  # Adjusted width
            height=10, # Adjusted height
            font=emoji_font,
            wrap=tk.WORD,
            relief=tk.FLAT  # Remove border
        )
        self.message_area.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)

        # Delay settings and input
        delay_frame = ttk.Frame(self.main_frame)
        delay_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(10, 0))
        ttk.Label(delay_frame, text="Delay (seconds):", font=('Segoe UI', 10)).grid(row=0, column=0, sticky=tk.W, padx=(0, 5))
        self.delay_var = tk.StringVar(value="5")
        self.delay_entry = ttk.Entry(delay_frame, textvariable=self.delay_var, width=10, font=('Segoe UI', 10))
        self.delay_entry.grid(row=0, column=1, sticky=tk.W)

        # Send button (placed next to delay entry)
        self.send_button = self.create_rounded_button(delay_frame, text="Send", command=self.start_sending, width=80, height=28)
        self.send_button.grid(row=0, column=2, sticky=tk.W, padx=5)


        # Status label (will be updated dynamically)
        self.status_var = tk.StringVar(value="")  # Start with empty status
        self.status_label = ttk.Label(self.main_frame, textvariable=self.status_var, font=('Segoe UI', 9), anchor=tk.CENTER)
        self.status_label.grid(row=4, column=0, sticky=(tk.W, tk.E), pady=5)

        self.is_sending = False

        # Configure pyautogui settings
        pyautogui.FAILSAFE = True
        pyautogui.PAUSE = 0.001

    # Modified methods to remove stop_sending functionality

    def start_sending(self):
        messages = self.message_area.get('1.0', tk.END).splitlines()
        if not messages or all(msg.strip() == '' for msg in messages):
            messagebox.showwarning("Warning", "No messages to send!")
            return

        try:
            delay = int(self.delay_var.get())  # Use int for the countdown
            if delay < 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid delay time!")
            return

        self.is_sending = True
        # self.send_button.state(['disabled']) # No longer needed with canvas button
        self.send_button.itemconfig('button_rect', fill='#d9d9d9')  # Disable effect - Lighter gray
        self.send_button.itemconfig('button_text', fill='gray')

        # Start sending in a separate thread
        self.send_thread = threading.Thread(target=self.send_messages, args=(messages, delay))
        self.send_thread.start()

    # Removed stop_sending method

    def send_messages(self, messages, delay):
        # Dynamic countdown
        for remaining in range(delay, 0, -1):
            self.status_var.set(f"Starting in {remaining} seconds... Focus your target window!")
            time.sleep(1)

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
            # self.send_button.state(['!disabled']) # No longer needed with canvas button
            self.send_button.itemconfig('button_rect', fill='#add8e6') # Re-enable effect - Light blue
            self.send_button.itemconfig('button_text', fill='black')

    def create_rounded_button(self, parent, text, command, width, height):
        canvas = tk.Canvas(parent, width=width, height=height, bg='#f0f0f0', highlightthickness=0)

        # Draw rounded rectangle with light blue fill
        radius = 10  # Adjust for roundness
        canvas.create_arc(0, 0, 2 * radius, 2 * radius, start=90, extent=90, fill='#add8e6', outline="", tags='button_rect')
        canvas.create_arc(width - 2 * radius, 0, width, 2 * radius, start=0, extent=90, fill='#add8e6', outline="", tags='button_rect')
        canvas.create_arc(0, height - 2 * radius, 2 * radius, height, start=180, extent=90, fill='#add8e6', outline="", tags='button_rect')
        canvas.create_arc(width - 2 * radius, height - 2 * radius, width, height, start=270, extent=90, fill='#add8e6', outline="", tags='button_rect')
        canvas.create_rectangle(radius, 0, width - radius, height, fill='#add8e6', outline="", tags='button_rect')
        canvas.create_rectangle(0, radius, width, height - radius, fill='#add8e6', outline="", tags='button_rect')

        # Add text
        canvas.create_text(width / 2, height / 2, text=text, font=('Segoe UI', 11), fill='black', tags='button_text')

        # Bind events for button-like behavior
        canvas.bind("<Button-1>", lambda event: command())
        canvas.bind("<Enter>", lambda event: canvas.itemconfig('button_rect', fill='#9ac7d5'))  # Hover effect - Slightly darker blue
        canvas.bind("<Leave>", lambda event: canvas.itemconfig('button_rect', fill='#add8e6'))

        return canvas

def main():
    root = tk.Tk()
    app = MessageSenderGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()