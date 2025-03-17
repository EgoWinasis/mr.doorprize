import tkinter as tk
from PIL import Image, ImageTk
import random
import time

# List to keep track of winners
winners = set()

# Function to generate and animate the 3-digit number
def start_doorprize():
    # Disable the start button during the animation
    start_button.config(state=tk.DISABLED)

    # Shuffle the cards' digits and show back of cards
    shuffle_cards()

    # Wait a bit for shuffle animation
    root.after(500, flip_cards)

    # Re-enable the start button after animation
    start_button.config(state=tk.NORMAL)

# Function to shuffle the digits randomly on each card
def shuffle_cards():
    # Show back of the card images during shuffle
    for i in range(3):
        card_canvas[i].itemconfig(card_image_canvas[i], image=card_back_photo)  # Show the back of the card

    # Randomly shuffle digits on cards
    for i, var in enumerate([digit_1, digit_2, digit_3]):
        var.set(random.randint(0, 9))

    # Move the cards to simulate shuffle effect
    for i in range(3):
        card_canvas[i].place(relx=random.uniform(0.3, 0.7), rely=random.uniform(0.4, 0.6))

    # Update the UI to show shuffle animation
    root.update()

# Function to flip the cards to reveal the final digits
def flip_cards():
    # Get random digits for the number
    final_number = [random.randint(0, 9) for _ in range(3)]

    # Shuffle until the number has not been won already
    while tuple(final_number) in winners:
        final_number = [random.randint(0, 9) for _ in range(3)]  # Generate new number if already won

    # Add the winner to the history
    winners.add(tuple(final_number))

    # Update the final digits in the cards
    digit_1.set(final_number[0])
    digit_2.set(final_number[1])
    digit_3.set(final_number[2])

    # Show the front of the card with the final digits
    for i, var in enumerate([digit_1, digit_2, digit_3]):
        card_canvas[i].itemconfig(card_image_canvas[i], image=card_images[final_number[i]])  # Show the final card

    # Reset card positions after flip animation
    reset_card_positions()

# Function to reset the card positions after flip animation
def reset_card_positions():
    for i in range(3):
        card_canvas[i].place(relx=0.4 + (i * 0.1), rely=0.5, anchor="center")

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
digit_1 = tk.IntVar(value=random.randint(0, 9))
digit_2 = tk.IntVar(value=random.randint(0, 9))
digit_3 = tk.IntVar(value=random.randint(0, 9))

# Load card images for 0-9 digits
card_images = []
for i in range(10):
    card_images.append(ImageTk.PhotoImage(Image.open(f"card/{i}.png")))

# Load the back of the card
card_back_image = Image.open("card/card_back.png")
card_back_photo = ImageTk.PhotoImage(card_back_image)

# Create a canvas to hold the card images
card_canvas = []
card_image_canvas = []

# Place 3 cards on the screen with back images initially
for i in range(3):
    card_canvas.append(tk.Canvas(root, width=100, height=150))
    card_canvas[i].place(relx=0.4 + (i * 0.1), rely=0.5, anchor="center")
    card_image_canvas.append(card_canvas[i].create_image(50, 75, image=card_back_photo))  # Initially showing back of cards

# Set up the start button
start_button = tk.Button(root, text="Start", font=("Helvetica", 32), command=start_doorprize, bg="green", fg="white")
start_button.place(relx=0.5, rely=0.8, anchor="center")

# Place the exit button at the top-right corner
exit_image = Image.open("image/close2.png")
exit_photo = ImageTk.PhotoImage(exit_image)
exit_button = tk.Button(root, image=exit_photo, command=close_app, bd=0)
exit_button.place(relx=0.95, rely=0.05, anchor="center")

# Place the history button next to the exit button
history_image = Image.open("image/winner.png")
history_photo = ImageTk.PhotoImage(history_image)
history_button = tk.Button(root, image=history_photo, command=show_history, bd=0)
history_button.place(relx=0.91, rely=0.05, anchor="center")

# Run the main loop
root.mainloop()
