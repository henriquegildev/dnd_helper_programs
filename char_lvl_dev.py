import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext, filedialog
from tkinter import font as tkFont
import csv
import os

# Global Variables
CHARACTER_NAME = "Default"  # Character name
SESSION_XP = 0  # Session XP
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
    result_xp_label.config(text=f"XP:")
    result_xp_value.config(text=f"{new_xp}/{xp_for_next_level}")
    last_xp_label.config(text=f"XP Gained:")
    last_xp_value.config(text=f"{gained_xp}")

    # Update the input fields with new values for ongoing progression
    current_xp_entry.delete(0, tk.END)
    current_xp_entry.insert(0, str(new_xp))
    current_level_entry.delete(0, tk.END)
    current_level_entry.insert(0, str(new_level))

    # Clear the gained XP entry
    gained_xp_entry.delete(0, tk.END)
    gained_xp_entry.insert(0, str(0))


# Function to save calculated XP to the selected magic
def save_calculated_xp():
    """
    Save the calculated experience points (XP) and level for the selected magic.
    This function updates the global SESSION_XP variable and saves the new level and XP
    for the selected magic. It also handles UI updates and error messages.
    Global Variables:
    - SESSION_XP: The total session XP accumulated.
    Raises:
    - ValueError: If the XP and level values are not valid numeric values.
    UI Elements:
    - result_level_value: Label containing the new level value.
    - result_xp_value: Label containing the new XP value in the format "current_xp/next_xp".
    - last_xp_value: Label containing the last XP value.
    - session_xp_value: Label to display the updated session XP.
    Error Messages:
    - "Invalid Data": Displayed if the XP and level values are not valid numeric values.
    - "No Magic Selected": Displayed if no magic is selected to save its data.
    Success Messages:
    - "Save Successful": Displayed when XP and level are saved successfully.
    UI Updates:
    - refresh_ui(): Refreshes the UI to show updated magic buttons.
    """
    global SESSION_XP

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

        if selected_magic_index == 0:
            SESSION_XP += int(last_xp_value.cget("text"))
            session_xp_value.config(text=f"{SESSION_XP}")
            skip_session_xp = True

        # Save the new level and XP for the selected magic
        update_magic_data(selected_magic_index, new_level, new_xp, next_xp, skip_session_xp)


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
    result_xp_label.config(text="XP: ")
    last_xp_label.config(text="XP Gained: ")

    # Reset the magic buttons' appearance
    for button in magic_buttons:
        button.config(bg=button_color, state=tk.NORMAL)


def reset_session_xp():
    global SESSION_XP
    # Pop up a confirmation dialog
    if not messagebox.askyesno("Reset Session XP", "Reset the session XP?"):
        return
    SESSION_XP = 0


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


def load_character_data(path=None, character_name=None, skip_session_xp=False):
    """
    Load character data from a CSV file based on the given character name.
    """
    global CHARACTER_NAME
    global SESSION_XP
    if character_name:
        CHARACTER_NAME = character_name
        file_path = f"character_data_{character_name.lower()}.csv"
    elif path:
        file_path = path
    else:
        file_path = "character_data_default.csv"  # Default file

    if os.path.exists(file_path):
        with open(file_path, mode="r") as file:
            reader = csv.reader(file)
            char_data = list(reader)
            CHARACTER_NAME = char_data[0][0]  # Get the character name from the data
            if skip_session_xp == False:
                SESSION_XP = int(char_data[0][1])  # Get the session XP from the data
            return char_data[2:]  # Skip header and character name
    else:
        # If file doesn't exist, create default data
        messagebox.showinfo(
            "File Not Found",
            f"No data found for {character_name}. Creating default character data.",
        )
        save_character_data(DEFAULT_CHAR_DATA, name=character_name)
        return DEFAULT_CHAR_DATA


def load_char_list():
    """
    Return a list of character names based on available CSV files.
    """
    char_list = []
    for file in os.listdir():
        if file.startswith("character_data_") and file.endswith(".csv"):
            char_name = file.replace("character_data_", "").replace(".csv", "")
            char_list.append(char_name)
    char_list.sort()  # Sort the list alphabetically
    return char_list


# Save character data to CSV
def save_character_data(data, name=CHARACTER_NAME):
    global CHARACTER_NAME
    global SESSION_XP
    with open(f"character_data_{name.lower()}.csv", mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([name, SESSION_XP])  # Write character name
        writer.writerow(
            ["magic", "magic_level", "exp", "current_exp", "next_exp"]
        )  # Write header
        writer.writerows(data)  # Write default or updated character data



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
            writer.writerow([CHARACTER_NAME, SESSION_XP])  # Write character name
            writer.writerows(DEFAULT_CHAR_DATA)  # Write default character data
    return path


def create_new_character_data():
    global CHARACTER_NAME
    CHARACTER_NAME = simpledialog.askstring("Character Name", "Enter Character Name:")
    if CHARACTER_NAME:
        # Prompt: create default file or edit default
        if messagebox.askyesno("Create New Character Data", "Edit new character data?"):
            path = create_character_data()
            # Open edit window
            save_character_data(name=CHARACTER_NAME)
            if path:
                refresh_ui()  # Refresh the UI to show the new character data
        else:
            messagebox.showerror("Error", "No file selected to save character data.")
    else:
        messagebox.showerror("Error", "Character name cannot be empty.")


# Load magic data from CSV and create magic buttons dynamically
def create_magic_buttons():
    """
    Creates and displays magic buttons for each magic entry in the character data.
    This function performs the following steps:
    1. Checks if the global CHARACTER_NAME is "Default" and loads the character list and data for the first character.
       Otherwise, it loads the data for the specified CHARACTER_NAME.
    2. Updates the character name label and session XP label with the current values.
    3. Clears any previously created magic buttons.
    4. Creates a new frame to hold the magic buttons.
    5. Iterates through the character data and creates a button for each valid magic entry.
       Each button displays the magic name and level, and is configured to load the magic data when clicked.
    6. Updates the window size based on the number of magic buttons created.
    Globals:
        selected_magic_index (int or None): Index of the selected magic button.
        CHARACTER_NAME (str): Name of the character.
        SESSION_XP (int): Current session experience points.
        magic_buttons (list): List to store references to the created magic buttons.
        main_frame (tk.Frame): Main frame of the application.
        bg_color (str): Background color for the buttons.
        button_color (str): Button color.
        dnd_font (tk.Font): Font used for the buttons.
    Returns:
        None
    """
    global selected_magic_index  # Keep track of the selected magic button index
    global CHARACTER_NAME
    global SESSION_XP

    selected_magic_index = None

    # Load character list and load the data from the first
    if CHARACTER_NAME == "Default":
        char_list = load_char_list()

        char_data = load_character_data(
            character_name=char_list[0]
        )  # Load character data
    else:
        char_data = load_character_data(character_name=CHARACTER_NAME)
    character_name_label.config(text=f"{CHARACTER_NAME}")  # Update character name label
    session_xp_value.config(text=f"{SESSION_XP}")  # Update session XP label

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
        magic_button.grid(row=idx, column=0, padx=5, pady=5, sticky="ew")
        magic_buttons.append(magic_button)  # Store reference to the button

    update_window_size()  # Update the window size based on the number of magic buttons


def char_list_buttons(last_button=11):
    char_list = load_char_list()  # Load available character names
    char_list_window = tk.Toplevel(root)
    char_list_window.title("Character List")
    char_list_window.geometry("300x400")
    char_list_window.configure(bg=bg_color)

    tk.Label(
        char_list_window,
        text="Select a Character",
        bg=bg_color,
        fg=fg_color,
        font=dnd_font,
    ).pack(pady=10)

    # Create new character data button
    new_char_button = tk.Button(
        char_list_window,
        text="New Character",
        command=create_new_character_data,
        bg=button_color,
        fg=bg_color,
    )

    for char in char_list:
        char_button = tk.Button(
            char_list_window,
            text=char.capitalize(),
            command=lambda char=char: select_character(char, char_list_window),
            bg=button_color,
            fg=bg_color,
            font=dnd_font,
        )
        char_button.pack(fill=tk.X, padx=10, pady=5)

    new_char_button.pack(pady=10)


def select_character(character_name, window):
    """
    Handle character selection, load data, and refresh UI.
    """
    window.destroy()  # Close the character list window
    load_character_data(character_name=character_name)  # Load character data
    create_magic_buttons()  # Refresh magic buttons
    character_name_label.config(text=f"{CHARACTER_NAME}")  # Update UI
    session_xp_value.config(text=f"{SESSION_XP}")  # Update UI


def load_and_close(char, window):
    """Load the selected character's data and close the character list window."""
    load_character_data(character_name=char)  # Load the selected character's data
    refresh_ui()  # Refresh the main UI
    window.destroy()  # Close the character list window


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
    result_xp_label.config(text=f"XP: ")
    result_xp_value.config(text=f"{exp}/{next_exp}")


# Function to update magic data in the CSV
def update_magic_data(index, new_level, new_xp, next_xp, skip_session_xp):
    """
    Update the magic data in the CSV file based on the given index and new values.
    """
    char_data = load_character_data(character_name=CHARACTER_NAME, skip_session_xp=skip_session_xp)
    char_data[index][1] = str(new_level)  # Update magic level
    char_data[index][2] = str(new_xp)  # Update current XP
    char_data[index][3] = str(next_xp)  # Update next XP


    # Save back to the CSV file
    save_character_data(char_data, CHARACTER_NAME)


# Function to refresh the UI to show updated magic buttons
def refresh_ui():
    # Clear the existing magic buttons
    for button in magic_buttons:
        button.destroy()
    magic_buttons.clear()
    session_xp_value.config(text=f"{SESSION_XP}")  # Update session XP

    # Recreate the magic buttons
    create_magic_buttons()


# Function to update window size based on the number of magic buttons
def update_window_size():
    num_buttons = len(magic_buttons)
    button_height = 50  # Height of each button
    # Calculate total height (accounting for padding)
    new_height = 490 if num_buttons == 0 else 90 + (num_buttons * button_height)
    root.geometry(f"460x{new_height}")


# Edit Character Data button
def edit_character_data(character=None):
    if character:
        char_data = load_character_data(character_name=character)
    else:
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
root.geometry("800x600")  # Set initial window size

# Colors
# White: #FFFFFF
bg_color = "#2C2F33"
button_color = "#262626"
fg_color = "#FFFFFF"

# Custom font
dnd_font = tkFont.Font(family="Helvetica", size=12)

# Ratio lock variable
ratio_lock = True

# Main frame
main_frame = tk.Frame(root, bg=bg_color)
main_frame.pack(fill=tk.BOTH, expand=True)

# Character name
character_name_label = tk.Label(
    main_frame, text=f"{CHARACTER_NAME}", bg=bg_color, fg=fg_color, font=dnd_font
)
character_name_label.grid(row=0, column=0, columnspan=1, pady=5)
character_name_label.config(font=("Helvetica", 24))

# Labels and entries for XP calculations
current_xp_label = tk.Label(
    main_frame, text="XP: ", bg=bg_color, fg=fg_color, font=dnd_font
)
# align center
current_xp_label.grid(row=0, column=1, sticky="ew", pady=5)

current_xp_entry = tk.Entry(main_frame, bg=bg_color, font=dnd_font, highlightbackground=fg_color, highlightcolor=fg_color, highlightthickness=1)
current_xp_entry.grid(row=0, column=2, sticky="ew", pady=5)

current_level_label = tk.Label(
    main_frame, text="Level: ", bg=bg_color, fg=fg_color, font=dnd_font
)
current_level_label.grid(row=1, column=1, sticky="ew", pady=5)
current_level_entry = tk.Entry(main_frame, bg=bg_color, font=dnd_font, highlightbackground=fg_color, highlightcolor=fg_color, highlightthickness=1)
current_level_entry.grid(row=1, column=2, sticky="ew", pady=5)

gained_xp_label = tk.Label(
    main_frame, text="Gained XP: ", bg=bg_color, fg=fg_color, font=dnd_font
)
gained_xp_label.grid(row=2, column=1, sticky="ew", pady=5)
gained_xp_entry = tk.Entry(main_frame, bg=bg_color, font=dnd_font, highlightbackground=fg_color, highlightcolor=fg_color, highlightthickness=1)
gained_xp_entry.grid(row=2, column=2, sticky="ew", pady=5)

# Result labels
result_level_label = tk.Label(
    main_frame, text="New Level: ", bg=bg_color, fg=fg_color, font=dnd_font
)
result_level_label.grid(row=3, column=1, sticky="ew", pady=5)

result_level_value = tk.Label(
    main_frame, text="", bg=bg_color, fg=fg_color, font=dnd_font
)
result_level_value.grid(row=3, column=2, sticky="ew", pady=5)

result_xp_label = tk.Label(
    main_frame, text="XP: ", bg=bg_color, fg=fg_color, font=dnd_font
)
result_xp_label.grid(row=4, column=1, sticky="ew", pady=5)

result_xp_value = tk.Label(main_frame, text="", bg=bg_color, fg=fg_color, font=dnd_font)
result_xp_value.grid(row=4, column=2, sticky="ew", pady=5)

last_xp_label = tk.Label(
    main_frame, text="XP Gained: ", bg=bg_color, fg=fg_color, font=dnd_font
)
last_xp_label.grid(row=5, column=1, sticky="ew", pady=5)

last_xp_value = tk.Label(main_frame, text="", bg=bg_color, fg=fg_color, font=dnd_font)
last_xp_value.grid(row=5, column=2, sticky="w", pady=5)


session_xp_label = tk.Label(
    main_frame, text="Session XP: ", bg=bg_color, fg=fg_color, font=dnd_font
)
session_xp_label.grid(row=6, column=1, sticky="ew", pady=5, padx=5)
session_xp_value = tk.Label(
    main_frame, text=f"{SESSION_XP}", bg=bg_color, fg=fg_color, font=dnd_font
)
session_xp_value.grid(row=6, column=2, sticky="w", pady=5, padx=5)  


# Buttons
calculate_button = tk.Button(
    main_frame,
    text="Calculate",
    command=calculate,
    bg=button_color,
    fg=bg_color,
)
calculate_button.grid(row=7, column=1, pady=5, padx=5, sticky="e")

reset_button = tk.Button(
    main_frame, text="Reset", command=reset_fields, bg=button_color, fg=bg_color
)
reset_button.grid(row=7, column=2, pady=5, padx=5, sticky="e")

multiplier_button = tk.Button(
    main_frame,
    text=f"Multiplier: {multiplier}x",
    command=toggle_multiplier,
    bg=button_color,
    fg=bg_color,
)
multiplier_button.grid(row=8, column=1, columnspan=2, padx=5,pady=5)

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
edit_button.grid(row=9, column=1, columnspan=2, padx=5, pady=5)

# Save XP button
save_xp_button = tk.Button(
    main_frame,
    text="Save XP",
    command=save_calculated_xp,
    bg=button_color,
    fg=bg_color,
)
save_xp_button.grid(row=10, column=1, columnspan=2, padx=5,pady=5)

reset_session_xp_button = tk.Button(
    main_frame,
    text="Reset SXP",
    command=reset_session_xp,
    bg=button_color,
    fg=bg_color,
)
reset_session_xp_button.grid(row=11, column=1, columnspan=2, padx=5,pady=5)


# Character lists buttons
char_list_button = tk.Button(
    main_frame,
    text="Character List",
    command=char_list_buttons,
    bg=button_color,
    fg=bg_color,
)
char_list_button.grid(row=11, column=0, columnspan=1, pady=0)

for i in range(13):
    main_frame.grid_rowconfigure(i, weight=1)
    main_frame.grid_columnconfigure(i, weight=1)


# Bind the configure event to maintain aspect ratio
root.bind("<Configure>")

root.mainloop()

