import tkinter as tk
from tkinter import messagebox
import sys

class CountdownApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Countdown Timer")
        self.root.geometry("480x525")
        self.root.resizable(False, False)
        
        # Initial time (25 minutes in seconds)
        self.initial_time = 60
        self.remaining_time = self.initial_time
        self.is_running = False
        self.notified_5min = False
        self.notified_1min = False
        self.timeout_popup = None
        
        # Timer display
        self.timer_label = tk.Label(root, text="25:00", font=("Helvetica", 48))
        self.timer_label.pack(pady=100)
        
        # Buttons frame
        button_frame = tk.Frame(root)
        button_frame.pack(pady=20)
        
        # Extend Time button
        self.extend_button = tk.Button(
            button_frame, 
            text="Extend Time", 
            command=self.show_extend_options,
            font=("Helvetica", 14),
            width=10,
            height=2
        )
        self.extend_button.pack(side=tk.LEFT, padx=20)
        
        # Pa Sukli button
        self.pa_sukli_button = tk.Button(
            button_frame, 
            text="Pa Sukli", 
            command=self.pa_sukli,
            font=("Helvetica", 14),
            width=10,
            height=2
        )
        self.pa_sukli_button.pack(side=tk.LEFT, padx=20)
        
        # Start/Stop button
        self.start_stop_button = tk.Button(
            root, 
            text="Start", 
            command=self.start_stop_timer,
            font=("Helvetica", 14),
            width=10,
            height=2
        )
        self.start_stop_button.pack(pady=20)
        
        # Timer update
        self.update_timer()
        
    def show_extend_options(self):
        # If timeout popup is showing, close it first
        if self.timeout_popup:
            self.timeout_popup.destroy()
            self.timeout_popup = None
            self.is_running = True
            self.start_stop_button.config(text="Stop")
        
        # Create popup window
        popup = tk.Toplevel(self.root)
        popup.title("Extend Time")
        popup.geometry("300x250")
        popup.resizable(False, False)
        
        # Center the popup relative to main window
        x = self.root.winfo_x() + (self.root.winfo_width() // 2) - 150
        y = self.root.winfo_y() + (self.root.winfo_height() // 2) - 125
        popup.geometry(f"+{x}+{y}")
        
        # Add title label
        tk.Label(popup, text="Select Extension:", font=("Helvetica", 14)).pack(pady=10)
        
        # Add extension options
        options = [
            ("5 pesos (25 mins)", 25 * 60),
            ("10 pesos (50 mins)", 50 * 60),
            ("15 pesos (1hr 15mins)", 75 * 60),
            ("20 pesos (1hr 40mins)", 100 * 60)
        ]
        
        for text, seconds in options:
            btn = tk.Button(
                popup,
                text=text,
                command=lambda s=seconds: self.extend_time(s, popup),
                font=("Helvetica", 12),
                width=25,
                pady=5
            )
            btn.pack(pady=5)
    
    def show_timeout_popup(self):
        # Create fullscreen popup
        self.timeout_popup = tk.Toplevel(self.root)
        self.timeout_popup.attributes('-fullscreen', True)
        self.timeout_popup.attributes('-topmost', True)
        
        # Disable window manager controls
        self.timeout_popup.overrideredirect(True)
        
        # Add message
        message = tk.Label(
            self.timeout_popup,
            text="YOUR TIME IS OVER!\nPLEASE INSERT COIN TO CONTINUE",
            font=("Helvetica", 48, 'bold'),
            fg='red',
            bg='black'
        )
        message.pack(expand=True, fill='both')
        
        # Center the message
        message.place(relx=0.5, rely=0.5, anchor='center')
        
        # Make the background black
        self.timeout_popup.config(bg='black')
        
        # Disable all other controls
        self.is_running = False
        self.start_stop_button.config(state='disabled')
        self.pa_sukli_button.config(state='disabled')
    
    def extend_time(self, seconds_to_add, popup=None):
        # Add selected time to the timer
        self.remaining_time += seconds_to_add
        
        # Update display
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
        
        # Reset notifications if we extended beyond the thresholds
        if self.remaining_time > 5 * 60:
            self.notified_5min = False
        if self.remaining_time > 60:
            self.notified_1min = False
        
        # Close the popup if it exists
        if popup:
            popup.destroy()
        
        # Re-enable controls if they were disabled
        self.start_stop_button.config(state='normal')
        self.pa_sukli_button.config(state='normal')
    
    def update_timer(self):
        if self.is_running and self.remaining_time > 0:
            # Check for notifications before decrementing time
            if not self.notified_5min and self.remaining_time <= 5 * 60:
                self.notified_5min = True
                self.root.after(100, self.show_notification, "You have 5 mins left")
            
            if not self.notified_1min and self.remaining_time <= 60:
                self.notified_1min = True
                self.root.after(100, self.show_notification, "You have 1 min left")
            
            # Decrement time
            self.remaining_time -= 1
            
            # Update display
            minutes = self.remaining_time // 60
            seconds = self.remaining_time % 60
            self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
        
        elif self.is_running and self.remaining_time <= 0 and not self.timeout_popup:
            self.is_running = False
            self.show_timeout_popup()
            
        # Schedule next update
        self.root.after(1000, self.update_timer)
    
    def show_notification(self, message):
        # This creates a non-modal messagebox that won't pause execution
        top = tk.Toplevel(self.root)
        top.title("Time Alert")
        tk.Label(top, text=message, font=("Helvetica", 14)).pack(padx=20, pady=20)
        tk.Button(top, text="OK", command=top.destroy).pack(pady=10)
        # Position the popup near the main window
        x = self.root.winfo_x() + 100
        y = self.root.winfo_y() + 100
        top.geometry(f"+{x}+{y}")
    
    def start_stop_timer(self):
        if self.is_running:
            self.is_running = False
            self.start_stop_button.config(text="Start")
        else:
            self.is_running = True
            self.notified_5min = False
            self.notified_1min = False
            self.start_stop_button.config(text="Stop")
    
    def pa_sukli(self):
        # Reset to initial time
        self.remaining_time = self.initial_time
        minutes = self.remaining_time // 60
        seconds = self.remaining_time % 60
        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")
        self.is_running = False
        self.notified_5min = False
        self.notified_1min = False
        self.start_stop_button.config(text="Start")

if __name__ == "__main__":
    root = tk.Tk()
    app = CountdownApp(root)
    root.mainloop()
