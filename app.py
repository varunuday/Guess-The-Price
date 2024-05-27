#Purpose: Guess the Price GUI

import tkinter as tk
from tkinter import PhotoImage, messagebox
import random
from PIL import Image, ImageTk
from list import items, luxury, entertainment, everyday

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Global variables to keep track of game count, used items, and total score
game_count = 0
used_items = []
total_score = 0
average_accuracies = []

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Function to create a new window for selecting category
def select_category():
    global average_accuracies
    main.withdraw()

    # Create a new Tkinter window for selecting category
    category_window = tk.Toplevel()
    category_window.title("Select Category")
    category_window.geometry("400x300")
    category_window.configure(bg="#ADD8E6")
    average_accuracies = []

    # Function to start the game with selected category
    def start_game_with_category():
        global used_items, game_count, total_score
        selected_category = category_var.get()
        if selected_category == 0:
            messagebox.showerror("Error", "Please select a category.")
            return

        if selected_category == 1:
            selected_items = items
        elif selected_category == 2:
            selected_items = luxury
        elif selected_category == 3:
            selected_items = entertainment
        elif selected_category == 4:
            selected_items = everyday

        category_window.withdraw()
        game_count = 0
        used_items = []
        total_score = 0
        start_game(selected_items)

    # Create and place a label for selecting category
    choose_the_topic_image = PhotoImage(file="choose_the_topic.png")
    category_label = tk.Label(category_window,
                              image=choose_the_topic_image,
                              bg="#ADD8E6")
    category_label.pack(pady=10)

    # Create a radio button for each category
    category_var = tk.IntVar()
    categories = [("Random", 1),
                  ("Luxury", 2),
                  ("Entertainment", 3),
                  ("Everyday Essentials", 4)]

    for category, value in categories:
        category_radio = tk.Radiobutton(category_window,
                                        text=category,
                                        variable=category_var,
                                        value=value,
                                        font=("Arial", 10),
                                        bg="#ADD8E6")
        category_radio.pack(side="top", anchor="w", padx=20, pady=5)

    # Create and place a button to start the game with selected category
    start_button = tk.Button(category_window,
                             text="Start Game",
                             font=("Arial", 10),
                             command=start_game_with_category)
    start_button.pack(pady=10)

    # Run the category window's main loop
    category_window.mainloop()
#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Define add_commas function outside start_game
def add_commas(event):
    global guess_entry
    value = guess_entry.get().replace(',', '')
    # Limit the length of the input to 12 characters
    if len(value) >= 12:
        value = value[:12]
    if value.isdigit():
        guess_entry.delete(0, tk.END)
        guess_entry.insert(0, "{:,}".format(int(value)))

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Function to create a new window for the game
def start_game(selected_items):
    global game_count, used_items, user_guess, actual_price, guess_entry, total_score

    # Quit if the game has already been played 10 times
    if game_count >= 10:
        show_game_over_window()
        return
    else:
        average_accuracy = 0

    # Find out the average accuracy
    average_accuracy = sum(average_accuracies) / len(average_accuracies) if average_accuracies else 0
    
    # Create a new Tkinter window for the game
    game_window = tk.Toplevel()
    game_window.title("Guess the Price - Game")
    game_window.geometry("750x600")
    game_window.configure(bg="#ADD8E6")

    # Determine the round number
    round_number = f"Round {game_count + 1}"

    # Create and place a label for the round number
    round_label = tk.Label(game_window, 
                           text=round_number, 
                           font=("Arial", 15, "bold"), 
                           bg="#ADD8E6")

    round_label.place(relx=0.99, rely=0.2, anchor="e") 

    # Create and place a label for the accuracy percentage
    accuracy_label = tk.Label(game_window,
                          text=f"Accuracy: \n{average_accuracy:.0f}%",
                          font=("Arial", 15, "bold"),
                          bg="#ADD8E6")
    accuracy_label.place(relx=1, rely=0.35, anchor="e")

    # Create and place a label for the score number
    score_label = tk.Label(game_window, 
                           text=f"Score: \n{total_score}", 
                           font=("Arial", 15, "bold"), 
                           bg="#ADD8E6")
    score_label.place(relx=0.99, rely=0.5, anchor="e")

    # Select a random item from the selected category that hasn't been used before
    item = random.choice([i for i in selected_items if i not in used_items])

    # Add the current item to the list of used items
    used_items.append(item)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    # Function to handle checking the guess
    def check_guess():
        game_window.withdraw()
        global game_count, user_guess, actual_price, total_score

        # Get the user's guess from the entry field
        user_guess = guess_entry.get()

        # Remove commas if present
        user_guess = user_guess.replace(',', '')

        # Perform validation checks on the guess
        if user_guess.isdigit() and int(user_guess) >= 0:

            # Convert the actual price to an integer
            actual_price = int(item['price'].strip('$'))

            # Calculate the difference between the user's guess and the actual price
            difference = int(user_guess) - actual_price

            # Calculate accuracy percentage
            accuracy = max(0, 100 - (abs(difference) / actual_price * 100))

            # Calculate the score based on the difference
            if difference == 0:
                score = 1000
            else:
                score = max(1, round(accuracy * 10))

            # Append accuracy to the list
            average_accuracies.append(accuracy) 

            # Add up to the total score
            total_score += score

            # Display the message to display
            message = f"You Guessed: \n${int(user_guess):,}\n"
            message += f"\nActual Price: \n${actual_price:,}\n"
            if difference == 0:
                message += "Congratulations! \nYou have guessed the exact price of the item!"
                message += f"\nAmount Off: \n${difference:,}.\n"
                message += f"\nAccuracy: {accuracy:.2f}%"
                message += f"\nScore: {score}\nTotal Score: {total_score}"
            else:
                message += f"\nAmount Off: \n${difference:,}.\n"
                message += f"\nAccuracy: {accuracy:.2f}%"
                message += f"\nScore: {score}\nTotal Score: {total_score}"

            # Create stats window
            stats_window = tk.Toplevel()
            stats_window.title("Game Stats")
            stats_window.geometry("375x335")
            stats_window.configure(bg="#ADD8E6")
            stats_label = tk.Label(stats_window,
                                text=message,
                                font=("Arial", 12, "bold"),
                                bg="#ADD8E6")
            stats_label.pack(pady=10)
            ok_button = tk.Button(stats_window,
                                text="NEXT ROUND",
                                font=("Arial", 10),
                                command=lambda: [stats_window.destroy(), game_window.destroy(), start_game(selected_items)],
                                width=20)
            ok_button.pack(side="bottom", anchor="center", padx=20, pady=20)
            # Increment the game count
            game_count += 1
        else:
            game_window.deiconify()
            messagebox.showerror("Error", "Please enter a valid positive number.")

    # Create and place a label for the item title
    title_label = tk.Label(game_window,
                           text=item['title'],
                           font=("Arial", 15, "bold"),
                           bg="#ADD8E6")
    title_label.pack(padx=5)

    additional_info_title_label = tk.Label(game_window,
                                           text="Additional Info",
                                           font=("Arial", 13, "bold"),
                                           bg="#ADD8E6")
    additional_info_title_label.pack(pady=5)

    # Create and place a label for the item fact
    fact_label = tk.Label(game_window,
                          text=item['fact'],
                          font=("Arial", 12),
                          bg="#ADD8E6")
    fact_label.pack(pady=5)

    # Create and place a label for the item image
    item_image = Image.open(item['image'])
    item_image = item_image.resize((300, 300))
    item_image = ImageTk.PhotoImage(item_image)
    image_label = tk.Label(game_window, image=item_image)
    image_label.pack(pady=10)

    # Create and place a label for the guess entry
    guess_label = tk.Label(game_window, text="Enter your guess:", font=("Arial", 10), bg="#ADD8E6")
    guess_label.pack(pady=10)

    # Create an entry field for the user's guess
    guess_entry = tk.Entry(game_window, 
                           font=("Arial", 12), 
                           width=20,
                           justify="center")
    guess_entry.pack()

    # Bind the entry widget to add_commas function for comma separation
    guess_entry.bind("<KeyRelease>", add_commas)

    # Create and place a button to check the guess
    check_button = tk.Button(game_window, text="Check", font=("Arial", 10), command=check_guess)
    check_button.pack(pady=10)

    # Run the game window's main loop
    game_window.mainloop()

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Function to create the game over window
def show_game_over_window():
    game_over_window = tk.Toplevel(main)
    game_over_window.title("Game Over")
    game_over_window.geometry("300x200")
    game_over_window.configure(bg="#ADD8E6")

    # Create and place a label for the game over message
    game_over_label = tk.Label(game_over_window,
                               text=f"Final Score: \n{total_score}",
                               font=("Impact", 20, "bold"),
                               bg="#ADD8E6")
    game_over_label.pack(pady=10)

    # Create and place a button to return to main menu
    menu_button = tk.Button(game_over_window,
                            text="Main Menu",
                            font=("Arial", 10),
                            command=lambda: [main.deiconify(), game_over_window.withdraw()])
    menu_button.pack(side="left", padx=20)

    # Create and place a button to quit
    quit_button = tk.Button(game_over_window,
                            text="Quit",
                            font=("Arial", 10),
                            command=main.destroy)
    quit_button.pack(side="right", padx=20)

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

def open_how_to_play_window():
    # Hides the main window when How to Play Menu Opens
    main.withdraw() 
    # Create a Tkinter Window
    how_to_play_window = tk.Toplevel(main)
    # Name the Window
    how_to_play_window.title("Game Overview")
    # Create a suitable window size
    how_to_play_window.geometry("850x400")
    # Make window background light blue
    how_to_play_window.configure(bg="#ADD8E6")

    # Create title font and place it onto window
    title_label = tk.Label(how_to_play_window,
                           text="Game Overview", 
                           font=("Arial", 14, "bold"), 
                           bg="#ADD8E6")
    title_label.pack(pady=10)

    # Create and pack each line of rules to make it neat
    objective_label = tk.Label(how_to_play_window, 
                               text="⚫ The objective of the game is to guess the price of various items as accurately as possible.", 
                               font=("Arial", 10), 
                               bg="#ADD8E6", 
                               justify="left")
    objective_label.pack(anchor="w", padx=20)

    mode_selection_label = tk.Label(how_to_play_window, 
                               text="⚫ You can choose between the four customized modes of Random, Luxury, Entertainment, and Everyday Essentials.", 
                               font=("Arial", 10), 
                               bg="#ADD8E6", 
                               justify="left")
    mode_selection_label.pack(anchor="w", padx=20)

    rounds_label = tk.Label(how_to_play_window, 
                            text="⚫ You will be given 10 rounds to predict these items. You can only type out 12 digit numbers. ", 
                            font=("Arial", 10), 
                            bg="#ADD8E6", 
                            justify="left")
    rounds_label.pack(anchor="w", padx=20)

    score_label = tk.Label(how_to_play_window, 
                           text="⚫ Your score is based on how close your guess is to the actual price. The closer the guess, the more points earned.", 
                           font=("Arial", 10), 
                           bg="#ADD8E6", 
                           justify="left")
    score_label.pack(anchor="w", padx=20)

    final_score_label = tk.Label(how_to_play_window, 
                                 text="⚫ The player's final score is the total accumulated points across all 10 rounds.", 
                                 font=("Arial", 10), 
                                 bg="#ADD8E6", 
                                 justify="left")
    final_score_label.pack(anchor="w", padx=20)

    feature_title = tk.Label(how_to_play_window,
                        text= "Features",
                        font=("Arial", 15, "bold"),
                        bg="#ADD8E6",
                        justify="left")
    
    feature_title.pack(pady=10)
    feature1 = tk.Label(how_to_play_window,
                        text= "⚫ Comma Separator: The game accepts large numbers with commas for easier readability.",
                        font=("Arial", 10),
                        bg="#ADD8E6",
                        justify="left")
    feature1.pack(anchor="w", padx=20)

    feature2 = tk.Label(how_to_play_window,
                        text= "⚫ Score Tracking: Your score is updated after each guess based on the accuracy of your prediction.",
                        font=("Arial", 10),
                        bg="#ADD8E6",
                        justify="left")
    feature2.pack(anchor="w", padx=20)

    feature3 = tk.Label(how_to_play_window,
                        text= "⚫ Accuracy Percentage: After each guess, your accuracy percentage" + 
                        " is displayed to indicate how close you were to the actual price.",
                        font=("Arial", 10),
                        bg="#ADD8E6",
                        justify="left")
    feature3.pack(anchor="w", padx=20)

    feature4 = tk.Label(how_to_play_window,
                        text= "⚫ There is a stats window after each guess" + 
                        " and it will provide insights for that guess.",
                        font=("Arial", 10),
                        bg="#ADD8E6",
                        justify="left")
    feature4.pack(anchor="w", padx=20)
    # Create a button to start the game
    start_game_button = tk.Button(how_to_play_window, 
                                  text="Start Game", 
                                  font=("Arial", 12), 
                                  bg="#FFFFFF", 
                                  command=lambda: [how_to_play_window.withdraw(), select_category()])
    start_game_button.pack(pady=10)

    # Create a button to go back to the main menu
    main_menu_button = tk.Button(how_to_play_window, 
                                 text="Main Menu", 
                                 font=("Arial", 12), 
                                 bg="#FFFFFF", 
                                 command=lambda: [how_to_play_window.destroy(), main.deiconify()])
    main_menu_button.pack(pady=10)
    

#-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Create the main window
main = tk.Tk()
main.title("Guess the Price")
main.geometry("400x350")
main.configure(bg="#ADD8E6")

# Create title label with image
title_image = PhotoImage(file="guesstheprice.png")
title_label = tk.Label(main, image=title_image, bg="#ADD8E6")
title_label.pack(pady=10)

# Create button frame
button_frame = tk.Frame(main, bg="#ADD8E6")
button_frame.pack()

# Button: 
play_image = PhotoImage(file="play_button.png")
play_button = tk.Button(button_frame, 
                        image=play_image, 
                        compound=tk.LEFT,
                        font=("Arial", 12),
                        command=select_category)
play_button.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

# Button: How to Play 
how_to_play_image = PhotoImage(file="how_to_play.png")
how_to_play_button = tk.Button(button_frame, 
                               image=how_to_play_image, 
                               compound=tk.LEFT, 
                               font=("Arial", 12), 
                               command=open_how_to_play_window)
how_to_play_button.grid(row=1, column=0, padx=10, pady=10, sticky='ew')

# Button: Quit
quit_image = PhotoImage(file="quit_button.png")
quit_button = tk.Button(button_frame, 
                        image=quit_image, 
                        compound=tk.LEFT, 
                        font=("Arial", 12),
                        command=main.withdraw)
quit_button.grid(row=2, column=0, padx=10, pady=10, sticky='ew')

# Run the tkinter main loop
main.mainloop()
