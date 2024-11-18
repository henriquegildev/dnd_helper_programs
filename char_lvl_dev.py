import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext, filedialog
from tkinter import font as tkFont
import csv
import os

# Initial multiplier value
multiplier = 10

# Store references to magic buttons to manage highlighting
magic_buttons = []

# Default character data if the CSV file does not exist
DEFAULT_CHAR_DATA = [
    ["CHAR", 1, 0, 10],
    ["FIRE", 1, 0, 10],
    ["BLACKSMITH", 1, 0, 10],
]


# Function to calculate the new level and XP
def calculate_level_and_xp(current_xp, current_level, gained_xp, multiplier):
    total_xp = current_xp + gained_xp
    new_level = current_level
    xp_for_next_level = multiplier * new_level

    # Calculate the new level
    while total_xp >= xp_for_next_level:
        new_level += 1
        total_xp -= xp_for_next_level
        xp_for_next_level = multiplier * new_level

    return new_level, total_xp, xp_for_next_level


# Function to handle the calculation and update UI
def calculate():
    try:
        current_xp = int(current_xp_entry.get())
        current_level = int(current_level_entry.get())
        gained_xp = int(gained_xp_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Please enter valid numeric values.")
        return

    new_level, new_xp, xp_for_next_level = calculate_level_and_xp(
        current_xp, current_level, gained_xp, multiplier
    )

    # Update the results labels
    result_level_label.config(text=f"New Level:")
    result_level_value.config(text=f"{new_level}")
    result_xp_label.config(text=f"Current XP:")
    result_xp_value.config(text=f"{new_xp}/{xp_for_next_level}")
    last_xp_label.config(text=f"Last XP Gained:")
    last_xp_value.config(text=f"{gained_xp}")

    # Update the input fields with new values for ongoing progression
    current_xp_entry.delete(0, tk.END)
    current_xp_entry.insert(0, str(new_xp))
    current_level_entry.delete(0, tk.END)
    current_level_entry.insert(0, str(new_level))

    # Clear the gained XP entry
    gained_xp_entry.delete(0, tk.END)


# Function to save calculated XP to the selected magic
def save_calculated_xp():
    # Ensure a magic is selected
    if selected_magic_index is not None:
        try:
            # Fetch values from the updated labels instead of entry fields
            new_level = int(result_level_value.cget("text"))
            new_xp = int(
                result_xp_value.cget("text").split("/")[0]
            )  # Get only the current XP
            next_xp = int(
                result_xp_value.cget("text").split("/")[1]
            )  # Get only the next XP
        except ValueError:
            messagebox.showerror(
                "Invalid Data", "Please enter valid numeric values for XP and level."
            )

            return

        # Save the new level and XP for the selected magic
        update_magic_data(selected_magic_index, new_level, new_xp, next_xp)
        messagebox.showinfo("Save Successful", "XP and Level saved successfully!")
    else:
        messagebox.showwarning(
            "No Magic Selected", "Please select a magic to save its data."
        )
    refresh_ui()  # Refresh the UI to show updated magic buttons


# Function to reset the inputs
def reset_fields():
    current_xp_entry.delete(0, tk.END)
    current_level_entry.delete(0, tk.END)
    gained_xp_entry.delete(0, tk.END)
    result_level_label.config(text="New Level: ")
    result_xp_label.config(text="Current XP: ")
    last_xp_label.config(text="Last XP Gained: ")

    # Reset the magic buttons' appearance
    for button in magic_buttons:
        button.config(bg=button_color, state=tk.NORMAL)


# Function to toggle the multiplier value
def toggle_multiplier():
    global multiplier
    # Cycle through the multipliers 1, 10, 100, 1000
    if multiplier == 1:
        multiplier = 10
    elif multiplier == 10:
        multiplier = 100
    elif multiplier == 100:
        multiplier = 1000
    else:
        multiplier = 1

    # Update the button label with the current multiplier value
    multiplier_button.config(text=f"Multiplier: {multiplier}x")


# Load character data from CSV or use default data if the file doesn't exist
def load_character_data(path="character_data.csv"):
    if os.path.exists(path):
        with open(path, mode="r") as file:
            reader = csv.reader(file)
            char_data = list(reader)
            return char_data[2:]  # Skip header and name of the character
    else:
        char_data = DEFAULT_CHAR_DATA
        save_character_data(char_data)  # Save default data to CSV
        return DEFAULT_CHAR_DATA


# Save character data to CSV
def save_character_data(data, name="CHARACTER"):
    with open("character_data.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name])  # Write character name
        writer.writerow(
            ["magic", "magic_level", "exp", "current_exp", "next_exp"]
        )  # Write header
        writer.writerows(data)  # Write default or updated character data


def get_character_data_path():
    # Get the path to the character data file

    # If more than one charecter_data[0-inf].csv file exists open the file dialog else use the existing the default
    if len([file for file in os.listdir() if file.startswith("character_data")]) > 1:
        path = filedialog.askopenfilename(
            initialdir=os.getcwd(),
            title="Select Character Data File",
            filetypes=[("CSV Files", "*.csv")],
        )
    else:
        path = "character_data.csv"
    return path


def create_character_data():
    # Create a new character data file
    path = filedialog.asksaveasfilename(
        initialdir=os.getcwd(),
        title="Save Character Data File",
        filetypes=[("CSV Files", "*.csv")],
        defaultextension=".csv",
    )
    if path:
        with open(path, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(
                ["magic", "magic_level", "exp", "current_exp", "next_exp"]
            )  # Write header
            writer.writerows(DEFAULT_CHAR_DATA)  # Write default character data
    return path


# Load magic data from CSV and create magic buttons dynamically
def create_magic_buttons():
    global selected_magic_index  # Keep track of the selected magic button index
    selected_magic_index = None

    path = get_character_data_path()

    char_data = load_character_data(path)

    # Clear previous magic buttons, if any
    for button in magic_buttons:
        button.destroy()
    magic_buttons.clear()

    magic_frame = tk.Frame(main_frame, bg=bg_color)
    magic_frame.grid(
        row=1, column=0, rowspan=9, padx=5, pady=5
    )  # Adjusted row and rowspan

    for idx, row in enumerate(char_data):
        if len(row) != 4:
            continue  # Skip invalid rows
        magic_name = row[0]  # Magic name
        magic_level = int(row[1])  # Magic level
        magic_exp = int(row[2])  # Magic current XP
        magic_next_exp = int(row[3])  # Magic next XP

        magic_button = tk.Button(
            magic_frame,
            text=f"{magic_name} LV{magic_level}",
            command=lambda idx=idx, lvl=magic_level, exp=magic_exp, next_exp=magic_next_exp: load_magic_data(
                idx, lvl, exp, next_exp
            ),
            bg=button_color,
            fg=bg_color,
            font=dnd_font,
        )
        magic_button.grid(row=idx, column=0, padx=10, pady=5, sticky="ew")
        magic_buttons.append(magic_button)  # Store reference to the button

    update_window_size()  # Update the window size based on the number of magic buttons


# Function to load magic data into input fields and highlight the button
def load_magic_data(index, level, exp, next_exp):
    global selected_magic_index
    selected_magic_index = index  # Set the currently selected magic index

    # Reset all buttons to their normal state
    for button in magic_buttons:
        button.config(bg=button_color, state=tk.NORMAL, fg=bg_color)

    # Grayout the selected magic button
    magic_buttons[index].config(
        bg="gray", state=tk.DISABLED, fg=bg_color
    )  # Grayed out color and unclickable

    current_xp_entry.delete(0, tk.END)
    current_xp_entry.insert(0, str(exp))
    gained_xp_entry.delete(0, tk.END)
    gained_xp_entry.insert(0, str(0))  # Assuming no gained XP when loading magic data
    current_level_entry.delete(0, tk.END)
    current_level_entry.insert(0, str(level))
    result_xp_label.config(text=f"Current XP: ")
    result_xp_value.config(text=f"{exp}/{next_exp}")


# Function to update magic data in the CSV
def update_magic_data(index, new_level, new_xp, next_xp):
    char_data = load_character_data()
    char_data[index][1] = str(new_level)  # Update magic level
    char_data[index][2] = str(new_xp)  # Update current XP
    char_data[index][3] = str(next_xp)  # Update next XP

    # Save back to the CSV file
    save_character_data(char_data)


# Function to refresh the UI to show updated magic buttons
def refresh_ui():
    # Clear the existing magic buttons
    for button in magic_buttons:
        button.destroy()
    magic_buttons.clear()

    # Recreate the magic buttons
    create_magic_buttons()


# Function to update window size based on the number of magic buttons
def update_window_size():
    num_buttons = len(magic_buttons)
    button_height = 40  # Height of each button
    # Calculate total height (accounting for padding)
    new_height = 600 if num_buttons == 0 else 120 + (num_buttons * button_height)
    root.geometry(f"550x{new_height}")


# Edit Character Data button
def edit_character_data():
    char_data = load_character_data()

    # Create a new window for editing character data
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Character Data")
    edit_window.geometry("400x400")

    # Create a scrolled text widget to display and edit character data
    text_area = scrolledtext.ScrolledText(
        edit_window, wrap=tk.WORD, width=50, height=20
    )
    text_area.pack(pady=10)

    # Prepare text for editing
    data_string = "\n".join([", ".join(row) for row in char_data])
    text_area.insert(tk.END, data_string)

    def save_character_data_and_refresh():
        # Get the modified text and split it into rows
        modified_data = text_area.get("1.0", tk.END).strip().splitlines()
        # Recreate the character data structure
        new_char_data = [line.split(", ") for line in modified_data]

        # Ensure proper formatting and save it
        save_character_data(new_char_data)
        refresh_ui()
        edit_window.destroy()  # Close the edit window

    # Save button
    save_button = tk.Button(
        edit_window, text="Save", command=save_character_data_and_refresh
    )
    save_button.pack(pady=5)


root = tk.Tk()
root.title("D&D XP Calculator")

# Colors
# White: #FFFFFF
bg_color = "#2C2F33"
button_color = "#262626"
fg_color = "#FFFFFF"

# Custom font
dnd_font = tkFont.Font(family="Helvetica", size=12)

# Title label
title_label = tk.Label(
    root, text="D&D XP Calculator", bg=bg_color, fg=fg_color, font=dnd_font
)
title_label.pack(fill=tk.X)

# Main frame
main_frame = tk.Frame(root, bg=bg_color)
main_frame.pack(fill=tk.BOTH, expand=True)

# UI Setup

# Labels and entries for XP calculations
current_xp_label = tk.Label(
    main_frame, text="Current XP: ", bg=bg_color, fg=fg_color, font=dnd_font
)
current_xp_label.grid(row=0, column=1, sticky="w", pady=5)
current_xp_entry = tk.Entry(main_frame, bg=bg_color, font=dnd_font)
current_xp_entry.grid(row=0, column=2, sticky="w", pady=5)

current_level_label = tk.Label(
    main_frame, text="Current Level: ", bg=bg_color, fg=fg_color, font=dnd_font
)
current_level_label.grid(row=1, column=1, sticky="w", pady=5)
current_level_entry = tk.Entry(main_frame, bg=bg_color, font=dnd_font)
current_level_entry.grid(row=1, column=2, sticky="w", pady=5)

gained_xp_label = tk.Label(
    main_frame, text="Gained XP: ", bg=bg_color, fg=fg_color, font=dnd_font
)
gained_xp_label.grid(row=2, column=1, sticky="w", pady=5)
gained_xp_entry = tk.Entry(main_frame, bg=bg_color, font=dnd_font)
gained_xp_entry.grid(row=2, column=2, sticky="w", pady=5)

# Result labels
result_level_label = tk.Label(
    main_frame, text="New Level: ", bg=bg_color, fg=fg_color, font=dnd_font
)
result_level_label.grid(row=3, column=1, sticky="w", pady=5)

result_level_value = tk.Label(
    main_frame, text="", bg=bg_color, fg=fg_color, font=dnd_font
)

result_level_value.grid(row=3, column=2, sticky="w", pady=5)

result_xp_label = tk.Label(
    main_frame, text="Current XP: ", bg=bg_color, fg=fg_color, font=dnd_font
)
result_xp_label.grid(row=4, column=1, sticky="w", pady=5)

result_xp_value = tk.Label(main_frame, text="", bg=bg_color, fg=fg_color, font=dnd_font)
result_xp_value.grid(row=4, column=2, sticky="w", pady=5)

last_xp_label = tk.Label(
    main_frame, text="Last XP Gained: ", bg=bg_color, fg=fg_color, font=dnd_font
)
last_xp_label.grid(row=5, column=1, sticky="w", pady=5)

last_xp_value = tk.Label(main_frame, text="", bg=bg_color, fg=fg_color, font=dnd_font)
last_xp_value.grid(row=5, column=2, sticky="w", pady=5)

# Buttons
calculate_button = tk.Button(
    main_frame,
    text="Calculate",
    command=calculate,
    bg=button_color,
    fg=bg_color,
)
calculate_button.grid(row=6, column=1, pady=5)

# Save button for saving calculated XP to the selected magic
# Save XP button


reset_button = tk.Button(
    main_frame, text="Reset", command=reset_fields, bg=button_color, fg=bg_color
)
reset_button.grid(row=6, column=2, pady=5)

multiplier_button = tk.Button(
    main_frame,
    text=f"Multiplier: {multiplier}x",
    command=toggle_multiplier,
    bg=button_color,
    fg=bg_color,
)
multiplier_button.grid(row=7, column=1, columnspan=2, pady=5)

# Create magic buttons dynamically based on CSV data
create_magic_buttons()

# Edit Character Data button
edit_button = tk.Button(
    main_frame,
    text="Edit Character Data",
    command=edit_character_data,
    bg=button_color,
    fg=bg_color,
)
edit_button.grid(row=8, column=1, columnspan=2, padx=5, pady=5)

# Save XP button
save_xp_button = tk.Button(
    main_frame,
    text="Save XP",
    command=save_calculated_xp,
    bg=button_color,
    fg=bg_color,
)
save_xp_button.grid(row=9, column=1, columnspan=2, pady=5)

# Initialize the main window
root.mainloop()