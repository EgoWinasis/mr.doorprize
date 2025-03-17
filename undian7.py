import tkinter as tk
from PIL import Image, ImageTk
import random
import time
import pygame
import mysql.connector
from mysql.connector import Error
from tkinter import messagebox


# MySQL connection configuration
db_config = {
    'host': '103.189.96.70',
    'user': 'egowinasis',
    'password': 'Ego21041003!',
    'database': 'doorprize_db',
    'port': 3308
}

# Global variables
db = None
cursor = None
winners = set()
available_numbers = []

def connect_to_database():
    """Connect to the MySQL database."""
    global db, cursor
    try:
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        print("Database connected successfully.")

    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        db = None  # Ensure db is None if connection fails
        cursor = None

def ensure_db_connection():
    """Ensure the database connection is active."""
    global db, cursor
    if db is None:
        print("Database not connected. Attempting to reconnect...")
        connect_to_database()
    else:
        try:
            db.ping(reconnect=True, attempts=3, delay=2)
            print("Database connection verified.")
        except mysql.connector.Error as err:
            print(f"Database connection error: {err}. Reconnecting...")
            if db:
                db.close()  # Close the existing connection
            connect_to_database()  # Reconnect


# Initialize pygame mixer for sound (before any sound is played)
pygame.mixer.init()


# Default settings
max_number = 450  # Default max number, this should be 3 digits (like 450)
shuffle_time = 0.05  # Default shuffle time in seconds

shuffling = False
total_animation_time = 3

# Fetch numbers from the database where kehadiran = 1
# Fetch numbers from the database where kehadiran = 1 and not in winners
def fetch_available_numbers():
    global available_numbers
    if cursor:
        try:
            
            query = """
                SELECT  peserta.no_undian 
                FROM peserta
                LEFT JOIN winners ON peserta.no_undian = winners.winner_number
                WHERE peserta.doorprize = 1 AND winners.winner_number IS NULL
            """
            cursor.execute(query)
            result = cursor.fetchall()
            available_numbers = [row[0] for row in result]  # Extract numbers into a list
            print("Available numbers fetched:", available_numbers)
        except mysql.connector.Error as err:
            print(f"Error fetching numbers from database: {err}")
    else:
        print("Database not connected. Unable to fetch numbers.")





# Fetch winners from the database on startup
def fetch_winners_from_db():
    global winners
    if cursor:
        try:
            cursor.execute("SELECT  winner_number FROM winners")
            result = cursor.fetchall()
            winners = {row[0] for row in result}  # Convert to a set
            print("Winners loaded from database:", winners)
        except mysql.connector.Error as err:
            print(f"Error fetching winners from database: {err}")
    else:
        print("Database not connected. Starting with an empty winners list.")

   

# Save a winner to the database
def save_winner_to_db(winner):
    ensure_db_connection()
    if cursor and db:
        try:
            cursor.execute("INSERT INTO winners (winner_number) VALUES (%s)", (winner,))
            db.commit()
            print(f"Winner {winner} saved to database.")
        except mysql.connector.Error as err:
            print(f"Error saving winner to database: {err}")



# Total animation time in seconds
total_animation_time = 10

# Shuffle time per step
shuffle_time = 0.1

# Function to generate and animate the 3-digit number
# Function to shuffle numbers
def shuffle_numbers():
    global shuffling

    if not shuffling:
        return  # Stop if the stop button was clicked

    digit_1.set(random.randint(0, 9))
    digit_2.set(random.randint(0, 9))
    digit_3.set(random.randint(0, 9))
    digit_35_1.set(3)  # Fixed
    digit_35_2.set(5)  # Fixed
    play_counting_sound()

    root.after(int(shuffle_time * 1000), shuffle_numbers)  # Continue shuffling



# Function to start/stop the process
def start_stop_doorprize(event=None):
    global shuffling

    if not shuffling:  # Start shuffling
        if not available_numbers:
            print("No more numbers to draw.")
            messagebox.showwarning("No Available Numbers", "No more numbers to draw.")
            start_button.config(state=tk.NORMAL)
            return

        shuffling = True
        start_button.config(text="Stop")  # Change button text
        shuffle_numbers()  # Start shuffling

    else:  # Stop and pick a winner
        shuffling = False
        start_button.config(text="Start", state=tk.DISABLED)  # Disable during final selection
        pick_winner()

# Function to pick a winner
def pick_winner():
    global available_numbers

    if not available_numbers:
        messagebox.showwarning("No Available Numbers", "No more numbers to draw.")
        start_button.config(state=tk.NORMAL, text="Start")
        return

    final_number = random.choice(available_numbers)

    while final_number in winners:
        available_numbers.remove(final_number)
        if not available_numbers:
            messagebox.showwarning("No Available Numbers", "No more numbers to draw.")
            start_button.config(state=tk.NORMAL, text="Start")
            return
        final_number = random.choice(available_numbers)

    available_numbers.remove(final_number)
    winners.add(final_number)
    save_winner_to_db(final_number)

    final_number_str = str(final_number).zfill(3)
    digit_1.set(int(final_number_str[0]))
    digit_2.set(int(final_number_str[1]))
    digit_3.set(int(final_number_str[2]))
    digit_35_1.set(3)
    digit_35_2.set(5)

    play_winner_sound()
    # Flicker the final number for emphasis
    # Add a 1-second delay before flickering the final number
    root.after(1500, flicker_final_number)

    start_button.config(state=tk.NORMAL, text="Start")  # Re-enable button


# Function to play the counting sound
def play_counting_sound():
    try:
        pygame.mixer.music.load("sound/count.wav")  # Load the counting sound file
        pygame.mixer.music.play()  # Play the counting sound
    except pygame.error as e:
        print(f"Error playing counting sound: {e}")


# Function to play the winner sound
def play_winner_sound():
    try:
        pygame.mixer.music.load("sound/winner.wav")  # Load the sound file
        pygame.mixer.music.play()  # Play the sound
    except pygame.error as e:
        print(f"Error playing sound: {e}")

# Function to flicker the digits during the shuffle
def flicker_digits():
    colors = ["black", "red", "blue", "green"]
    for widget in [card_1, card_2, card_3, card_35_1, card_35_2]:
        widget.config(fg=random.choice(colors))

# Function to flicker the final number for emphasis
def flicker_final_number():
    for _ in range(10):  # Flicker 10 times
        for widget in [card_1, card_2, card_3, card_35_1, card_35_2]:
            widget.config(fg="red")  # Highlight in red
        root.update()
        time.sleep(0.1)
        for widget in [card_1, card_2, card_3, card_35_1, card_35_2]:
            widget.config(fg="black")  # Back to black
        root.update()
        time.sleep(0.1)
# Function to open a new window showing the winner history
def show_history():
    history_window = tk.Toplevel(root)  # Create a new top-level window
    history_window.title("Data Pemenang")  # Title for the new window
    history_window.geometry("300x400")  # Size of the new window

    # Label for history window
    history_label = tk.Label(history_window, text="Data Pemenang", font=("Helvetica", 18))
    history_label.pack(pady=10)

    # Listbox to display the winner history
    history_listbox = tk.Listbox(history_window, font=("Helvetica", 14), fg="black", width=20, height=10, bg="white")
    history_listbox.pack(padx=10, pady=10)

    # Sort winners by order and append the new winner
    sorted_winners = sorted(map(int, winners))


    # Add all winners to the listbox
    for winner in sorted_winners:
        history_listbox.insert(tk.END, f"35{winner:03d}")


def show_peserta():
    history_window = tk.Toplevel(root)  # Create a new top-level window
    history_window.title("Data Peserta")  # Title for the new window
    history_window.geometry("300x400")  # Size of the new window

    # Label for history window
    history_label = tk.Label(history_window, text="Data Peserta", font=("Helvetica", 18))
    history_label.pack(pady=10)

    # Listbox to display the available_numbers history
    history_listbox = tk.Listbox(history_window, font=("Helvetica", 14), fg="black", width=20, height=10, bg="white")
    history_listbox.pack(padx=10, pady=10)

    # Sort available_numberss by order and append the new available_numbers
    sorted_available_numbers = sorted(map(int, available_numbers))


    # Add all available_numberss to the listbox
    for peserta in sorted_available_numbers:
        history_listbox.insert(tk.END, f"35{peserta:03d}")

def refresh_data():

    start_button.config(state=tk.DISABLED)
    
    
    global winners, available_numbers, db, cursor


    # Disable the start button during the animation
    # Clear the current data
    winners.clear()
    available_numbers.clear()
    print("Cleared winners and available numbers.")

    # Ensure database connection is reinitialized
    try:
        if db is not None:  # Check if `db` exists
            if db.is_connected():
                cursor.close()
                db.close()
        
        # Reconnect to the database
        db = mysql.connector.connect(**db_config)
        cursor = db.cursor()
        print("Database connection reestablished.")

        # Fetch fresh data
        fetch_available_numbers()
        fetch_winners_from_db()
        print("Refreshed data:")
        print("Winners:", winners)
        print("Available numbers:", available_numbers)
        
        # Show success alert
        root = tk.Tk()
        root.withdraw()  # Hide the root window
        messagebox.showinfo("Success", "Data refreshed successfully!")
        # Re-enable the start button
        start_button.config(state=tk.NORMAL)


    except mysql.connector.Error as e:
        print(f"Database error: {e}")
        db = None  # Ensure `db` is set to None if connection fails
        cursor = None


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
bg_image = Image.open("image/doorprize.png")
bg_photo = ImageTk.PhotoImage(bg_image)

# Set the background image
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)
# Create a frame to hold the three cards (digits)
card_frame = tk.Frame(root, bg="white", bd=0)  # Frame with no border

# Place the frame in the desired location
card_frame.place(relx=0.52, rely=0.6, anchor="center")

# Create StringVar for each digit to dynamically update
digit_35_1 = tk.IntVar(value=0)
digit_35_2 = tk.IntVar(value=0)
digit_1 = tk.IntVar(value=0)
digit_2 = tk.IntVar(value=0)
digit_3 = tk.IntVar(value=0)

# Create card-like labels for each digit inside the frame
card_1 = tk.Label(card_frame, textvariable=digit_1, font=("Helvetica", 128), fg="black", bg="white")
card_1.grid(row=0, column=3, padx=15, pady=13)  # Add padding between the cards

card_2 = tk.Label(card_frame, textvariable=digit_2, font=("Helvetica", 128), fg="black", bg="white")
card_2.grid(row=0, column=4, padx=15, pady=13)  # Add padding between the cards

card_3 = tk.Label(card_frame, textvariable=digit_3, font=("Helvetica", 128), fg="black", bg="white")
card_3.grid(row=0, column=5, padx=15, pady=13)  # Add padding between the cards

card_35_1 = tk.Label(card_frame, textvariable=digit_35_1, font=("Helvetica", 128), fg="black", bg="white")
card_35_1.grid(row=0, column=1, padx=15, pady=13)  # Add padding between the cards

card_35_2 = tk.Label(card_frame, textvariable=digit_35_2, font=("Helvetica", 128), fg="black", bg="white")
card_35_2.grid(row=0, column=2, padx=15, pady=13)  # Add padding between the cards


# Set up the start button
start_button = tk.Button(root, text="START", font=("Helvetica", 32), command=start_stop_doorprize, bg="green", fg="white")
start_button.place(relx=0.52, rely=0.86, anchor="center")


# Bind Enter key to start/stop function
root.bind("<Return>", start_stop_doorprize)  


# Place the exit button at the top-right corner
exit_image = Image.open("image/close2.png")
exit_photo = ImageTk.PhotoImage(exit_image)
exit_button = tk.Button(root, image=exit_photo, command=close_app, borderwidth=0, relief="flat", highlightthickness=0)
exit_button.place(relx=0.96, rely=0.05, anchor="center")

# Place the history button next to the exit button
history_image = Image.open("image/winner.png")
history_photo = ImageTk.PhotoImage(history_image)
history_button = tk.Button(root, image=history_photo, command=show_history, borderwidth=0, relief="flat", highlightthickness=0)
history_button.place(relx=0.92, rely=0.05, anchor="center")

# Place the peserta button next to the exit button
peserta_image = Image.open("image/peserta.png")
peserta_photo = ImageTk.PhotoImage(peserta_image)
peserta_button = tk.Button(root, image=peserta_photo, command=show_peserta, borderwidth=0, relief="flat", highlightthickness=0)
peserta_button.place(relx=0.88, rely=0.05, anchor="center")

# Add a new "Settings" button (with icon)
settings_image = Image.open("image/setting.png")
settings_photo = ImageTk.PhotoImage(settings_image)
settings_button = tk.Button(root, image=settings_photo, command=open_settings,borderwidth=0, relief="flat", highlightthickness=0)
settings_button.place(relx=0.84, rely=0.05, anchor="center")

# Add a new "refresh" button (with icon)
refresh_image = Image.open("image/refresh.png")
refresh_photo = ImageTk.PhotoImage(refresh_image)
refresh_button = tk.Button(root, image=refresh_photo, command=refresh_data,borderwidth=0, relief="flat", highlightthickness=0)
refresh_button.place(relx=0.80, rely=0.05, anchor="center")

# Run the main loop
root.mainloop()


# Close the database connection on exit
if cursor:
    cursor.close()
if db:
    db.close()