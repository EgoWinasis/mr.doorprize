import tkinter as tk
from PIL import Image, ImageTk
import random
import time

# Default settings
max_number = 450  # Default max number, this should be 3 digits (like 450)
shuffle_time = 0.05  # Default shuffle time in seconds

# List to keep track of winners
winners = set()

# Function to generate and animate the 3-digit number
def start_doorprize():
    # Disable the start button during the animation
    start_button.config(state=tk.DISABLED)

    # Generate a random number between 0 and max_number, ensuring it's a 3-digit number
    final_number = random.randint(0, max_number)

    # Shuffle the digits quickly in each "card"
    for _ in range(30):  # Run the shuffle 30 times
        digit_1.set(random.randint(0, 9))
        digit_2.set(random.randint(0, 9))
        digit_3.set(random.randint(0, 9))
        root.update()  # Update the GUI
        time.sleep(shuffle_time)  # Sleep for a short time to simulate animation

    # Generate the final 3-digit number (padded with zeros if necessary)
    final_number_str = str(final_number).zfill(3)

    # Ensure the final number is not a winner already
    while tuple(final_number_str) in winners:
        final_number = random.randint(0, max_number)  # Generate new number if already won
        final_number_str = str(final_number).zfill(3)

    # Add the winner to the history
    winners.add(tuple(final_number_str))

    # Update the final number in the cards
    digit_1.set(int(final_number_str[0]))
    digit_2.set(int(final_number_str[1]))
    digit_3.set(int(final_number_str[2]))

    # Re-enable the start button
    start_button.config(state=tk.NORMAL)

# Function to open a new window showing the winner history
def show_history():
    history_window = tk.Toplevel(root)  # Create a new top-level window
    history_window.title("Winner History")  # Title for the new window
    history_window.geometry("300x400")  # Size of the new window

    # Label for history window
    history_label = tk.Label(history_window, text="History of Winners", font=("Helvetica", 18))
    history_label.pack(pady=10)

    # Listbox to display the winner history
    history_listbox = tk.Listbox(history_window, font=("Helvetica", 14), fg="black", width=20, height=10, bg="white")
    history_listbox.pack(padx=10, pady=10)

    # Add the winners to the listbox
    for winner in winners:
        history_listbox.insert(tk.END, f"Winner: {''.join(map(str, winner))}")

# Function to close the application
def close_app():
    root.quit()

# Function to open the settings window and modify the max number and shuffle time
def open_settings():
    # Create a new settings window
    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("300x300")

    # Label for max number input
    max_number_label = tk.Label(settings_window, text="Max Number (3 digits):", font=("Helvetica", 14))
    max_number_label.pack(pady=10)

    # Entry for max number
    max_number_entry = tk.Entry(settings_window, font=("Helvetica", 14))
    max_number_entry.insert(0, str(max_number))  # Default value
    max_number_entry.pack(pady=10)

    # Label for shuffle time input
    shuffle_time_label = tk.Label(settings_window, text="Shuffle Time (s):", font=("Helvetica", 14))
    shuffle_time_label.pack(pady=10)

    # OptionMenu for selecting shuffle time
    shuffle_time_options = [5, 10, 15, 20]
    shuffle_time_var = tk.StringVar(settings_window)
    shuffle_time_var.set(str(int(shuffle_time * 100)))  # Convert to a whole number value (in seconds)
    shuffle_time_menu = tk.OptionMenu(settings_window, shuffle_time_var, *shuffle_time_options)
    shuffle_time_menu.pack(pady=10)

    # Function to save the new settings
    def save_settings():
        global max_number, shuffle_time
        max_number = int(max_number_entry.get())  # Update max number
        shuffle_time = int(shuffle_time_var.get())  # Update shuffle time
        shuffle_time = shuffle_time / 100  # Convert back to float seconds (as per original behavior)
        settings_window.destroy()  # Close settings window

    # Save button
    save_button = tk.Button(settings_window, text="Save", font=("Helvetica", 14), command=save_settings)
    save_button.pack(pady=20)

# Create the main window
root = tk.Tk()

# Make the window full screen
root.attributes("-fullscreen", True)

# Load the original background image
bg_image = Image.open("image/bg.png")
bg_photo = ImageTk.PhotoImage(bg_image)

# Set the background image
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

# Create StringVar for each digit to dynamically update
digit_1 = tk.IntVar(value=0)
digit_2 = tk.IntVar(value=0)
digit_3 = tk.IntVar(value=0)

# Create card-like labels for each digit directly on the main background
card_1 = tk.Label(root, textvariable=digit_1, font=("Helvetica", 128), fg="white", bg="blue", width=4, height=2, relief="solid", bd=5)
card_1.place(relx=0.2, rely=0.5, anchor="center")

card_2 = tk.Label(root, textvariable=digit_2, font=("Helvetica", 128), fg="white", bg="green", width=4, height=2, relief="solid", bd=5)
card_2.place(relx=0.5, rely=0.5, anchor="center")

card_3 = tk.Label(root, textvariable=digit_3, font=("Helvetica", 128), fg="white", bg="red", width=4, height=2, relief="solid", bd=5)
card_3.place(relx=0.8, rely=0.5, anchor="center")

# Set up the start button
start_button = tk.Button(root, text="START", font=("Helvetica", 32), command=start_doorprize, bg="green", fg="white")
start_button.place(relx=0.5, rely=0.8, anchor="center")

# Place the exit button at the top-right corner
exit_image = Image.open("image/close2.png")
exit_photo = ImageTk.PhotoImage(exit_image)
exit_button = tk.Button(root, image=exit_photo, command=close_app, borderwidth=0, relief="flat", highlightthickness=0)
exit_button.place(relx=0.95, rely=0.05, anchor="center")

# Place the history button next to the exit button
history_image = Image.open("image/winner.png")
history_photo = ImageTk.PhotoImage(history_image)
history_button = tk.Button(root, image=history_photo, command=show_history, borderwidth=0, relief="flat", highlightthickness=0)
history_button.place(relx=0.91, rely=0.05, anchor="center")

# Add a new "Settings" button (with icon)
settings_image = Image.open("image/setting.png")
settings_photo = ImageTk.PhotoImage(settings_image)
settings_button = tk.Button(root, image=settings_photo, command=open_settings,borderwidth=0, relief="flat", highlightthickness=0)
settings_button.place(relx=0.87, rely=0.05, anchor="center")

# Run the main loop
root.mainloop()
