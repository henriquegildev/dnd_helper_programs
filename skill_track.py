"""
    Author: Henrique Gil
    Description: Skill Tracking 1.0 and Char Level Calculator 1.0
    Version: 1.0

    Date: 26/01/2025
"""

import tkinter as tk
from tkinter import messagebox
import os
import csv

"""
Welcome to Skill Tracking 1.0:

Skill Tracking 1.0 update notes:
	-Multi Skill tracking.
	-Diferent cooldowns.
	-Easily Edit list of skills and cooldowns.
    -Now reads magic levels from character data.
    -Calculates power stacks and damage, by tracking the elements used in the skills.
    -Includes a buff stacking feature to manually input magic and damage buffs from other characters. Reset button included.
    -Magic levels are now displayed in the UI.
    -Activated skills are now displayed in the UI.
    -Added support for souls and pets skills.
    -Skills can now have a duration. This affects the activated skills list and the power stacking calculation.
    -Added a total damage calculation.
    -Skills having a Weapon 'element' means it is a doubling attack (i.e. dual strike), which now doubles the total damage. (This is a thing in our campaign)

Extras:
    -Fixed a bug where the skills were not being saved to the file properly.
    -Scaling of window size of the program is kind of working, but still needs some work.

Todos:
    -Add multiple characters support.
    -Fix scaling issues.
    -Implement DM Mode, where DMs can load multiple characters or player characters and track their skills usage and damage. (Probably a separate program)
    -Add instructions for executable creation. (for less technical users/windows users)
"""

# Define initial skill list
skills = []
bonus = []
skills_clean = []
activated_skills = []
magic_levels = {}

# Character name
CHARACTER_NAME = (
    "Default"  # Still need to implement multiple characters, change name accordingly
)

# File to store the skills
SKILL_FILE = f"skills_{CHARACTER_NAME.lower()}.csv"

# Magics
MAGICS = [
    "RADIANT",
    "LIGHT",
    "DARK",
    "FIRE",
    "WATER",
    "ICE",
    "NATURE",
    "LIGHTNING",
    "EARTH",
    "WIND",
    "WEAPON",
    "SOUL",
    "PET",
    "CHAR",
]

# Define colors
bg_color = "#2C2F33"
button_color = "#262626"
fg_color = "#FFFFFF"


# Function to load skills from a file
def load_skills():
    global skills
    global skills_clean
    global bonus
    if os.path.exists(SKILL_FILE):
        with open(SKILL_FILE, "r") as file:
            skills = []
            bonus = []
            for line in file:
                parts = line.strip().split(",")
                name = parts[0]
                # Check if cooldown is provided if not default to 3
                cooldown = int(parts[1]) if len(parts) > 1 else 3
                if len(parts) == 5:  # Has Element, bonus, and duration
                    skills.append(
                        {
                            "name": name,
                            "cooldown": cooldown,
                            "turns_left": 0,
                            "element": parts[2],
                            "bonus": parts[3],
                            "duration": parts[4],
                        }
                    )
                elif len(parts) == 4:  # Element bonus
                    skills.append(
                        {
                            "name": name,
                            "cooldown": cooldown,
                            "turns_left": 0,
                            "element": parts[2],
                            "bonus": parts[3],
                            "duration": 1,
                        }
                    )
                elif len(parts) == 3:  # Check if element is provided
                    skills.append(
                        {
                            "name": name,
                            "cooldown": cooldown,
                            "turns_left": 0,
                            "element": parts[2],
                            "bonus": None,
                            "duration": 1,
                        }
                    )
                elif len(parts) == 2:
                    if "{" in name:
                        element = name.split("{")[1].split("}")[0]
                        bonus.append({"element": element, "bonus": parts[1]})
                    else:
                        skills.append(
                            {
                                "name": name,
                                "cooldown": cooldown,
                                "turns_left": 0,
                                "element": None,
                                "bonus": None,
                                "duration": 1,
                            }
                        )
                        skills_clean.append(
                            {"name": name, "cooldown": cooldown, "turns_left": 0}
                        )
                elif len(parts) == 1:
                    if "{" in name:
                        continue
                    else:
                        skills.append({"name": name})  # Separator
    else:
        # Default skills if no file is found
        skills = [
            {
                "name": "Dual Strike",
                "cooldown": 3,
                "turns_left": 0,
                "element": "WEAPON",
                "bonus": 0,
                "duration": 1,
            },
            {
                "name": "Dodge",
                "cooldown": 3,
                "turns_left": 0,
                "element": "NONE",
                "bonus": 0,
                "duration": 1,
            },
            {
                "name": "Heal",
                "cooldown": 3,
                "turns_left": 0,
                "element": "EARTH",
                "bonus": 0,
                "duration": 1,
            },
            {
                "name": "Holy Sword",
                "cooldown": 3,
                "turns_left": 0,
                "element": "LIGHT",
                "bonus": 0,
                "duration": 1,
            },
            {
                "name": "Arrow of Light",
                "cooldown": 3,
                "turns_left": 0,
                "element": "LIGHT",
                "bonus": 0,
                "duration": 1,
            },
            {
                "name": "Flash",
                "cooldown": 3,
                "turns_left": 0,
                "element": "LIGHT",
                "bonus": 0,
                "duration": 1,
            },
            {
                "name": "Hell Spider",
                "cooldown": 3,
                "turns_left": 0,
                "element": "FIRE",
                "bonus": 0,
                "duration": 1,
            },
            {
                "name": "Purifying Wall",
                "cooldown": 3,
                "turns_left": 0,
                "element": "FIRE",
                "bonus": 0,
                "duration": 1,
            },
            {
                "name": "Divine Slash",
                "cooldown": 3,
                "turns_left": 0,
                "element": "WEAPON",
                "bonus": 0,
                "duration": 1,
            },
            {
                "name": "Sunshine Blessing",
                "cooldown": 3,
                "turns_left": 0,
                "element": "LIGHT",
                "bonus": 0,
                "duration": 1,
            },
            {
                "name": "Cruel Sun",
                "cooldown": 3,
                "turns_left": 0,
                "element": "FIRE",
                "bonus": 0,
                "duration": 1,
            },
            {
                "name": "Water Ball",
                "cooldown": 3,
                "turns_left": 0,
                "element": "WATER",
                "bonus": 0,
                "duration": 1,
            },
        ]

    # Clean skills list
    # If it has [,-, or { in the name, it's not a skill
    skills_clean = [
        s
        for s in skills
        if "[" not in s["name"] and "-" not in s["name"] and "{" not in s["name"]
    ]

    refresh_ui()


# Function to save skills to a file
def save_skills(skills):
    with open(SKILL_FILE, "w") as file:
        for skill in skills:
            if "[" in skill["name"]:
                file.write(f"{skill['name']}\n")
            elif "-" in skill["name"]:
                file.write(f"{skill['name']}\n")
            elif "{" in skill["name"]:
                # Separator
                if skill["name"] in MAGICS:
                    file.write(f"{skill['name']},{skill['bonus']}\n")
                else:
                    file.write(f"{skill['name']}\n")
            elif skill["element"] == "SOUL" or skill["element"] == "PET":
                file.write(f"{skill['name']},{skill['cooldown']},{skill['element']}\n")
            else:
                file.write(
                    f"{skill['name']},{skill['cooldown']},{skill['element']},{skill['bonus']},{skill['duration']}\n"
                )


# Function to update the skill timers and refresh the UI
def update_timers():
    for skill in skills_clean:
        if skill["turns_left"] > 0:
            skill["turns_left"] -= 1

    # Update activated skills duration
    for skill in activated_skills:
        skill_duration = int(skill["duration"])
        if skill_duration > 0:
            skill_duration -= 1
            skill["duration"] = skill_duration

    refresh_ui()


# Function to use a skill and start its timer
def use_skill(skill_index):
    skill = skills[skill_index]
    if int(skill.get("duration", 1)) > 100:
        # Toggle the skill
        skill["turns_left"] = 0 if skill["turns_left"] > 0 else skill["cooldown"]
    else:
        skill["turns_left"] = skill["cooldown"]
    refresh_ui()


# Function to refresh the UI
def refresh_ui():
    # Clear the existing skill label and button widgets if they exist
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Rebuild UI for each skill
    for i, skill in enumerate(skills):
        if "[" in skill["name"]:
            # Separator
            skill_var = tk.StringVar(value=f"{skill['name']}")
            skill_label = tk.Label(
                main_frame,
                textvariable=skill_var,
                font=("Arial", 12),
                bg=bg_color,
                fg=fg_color,
            )
            skill_label.grid(row=i, column=0, padx=5, pady=1, sticky="ew")
            continue
        elif "-" in skill["name"]:
            # Soul/Pet
            skill_var = tk.StringVar(value=f"{skill['name']}")
            skill_label = tk.Label(
                main_frame,
                textvariable=skill_var,
                font=("Arial", 12),
                bg=bg_color,
                fg=fg_color,
            )
            skill_label.grid(row=i, column=0, padx=5, pady=1, sticky="w")
            continue
        elif "{" in skill["name"]:
            # Bonus
            skill_var = tk.StringVar(value=f"{skill['name']}")
            skill_label = tk.Label(
                main_frame,
                textvariable=skill_var,
                font=("Arial", 12),
                bg=bg_color,
                fg=fg_color,
            )
            skill_label.grid(row=i, column=0, padx=5, pady=1, sticky="w")
            continue
        turns_left = skill["turns_left"]
        skill_var = tk.StringVar(value=f"{i+1}. {skill['name']}")

        skill_cooldown_label = tk.Label(
            main_frame,
            text=f"{turns_left}",
            font=("Arial", 12),
            bg=bg_color,
            fg=fg_color,
        )

        skill_label = tk.Label(
            main_frame,
            textvariable=skill_var,
            font=("Arial", 12),
            bg=bg_color,
            fg=fg_color,
        )

        skill_cooldown_label.grid(row=i, column=1, padx=5, pady=1, sticky="w")
        skill_label.grid(row=i, column=0, padx=5, pady=1, sticky="w")

        skill_button = tk.Button(
            main_frame,
            text=f"Use {skill['name']}",
            command=lambda i=i: use_skill(i),
            bg=button_color,
            fg=bg_color,
        )
        skill_button.grid(row=i, column=2, padx=5, pady=1)

        # Disable or enable button based on turns_left
        if turns_left == 0:
            skill_button.config(state="normal")
        else:
            skill_button.config(state="disabled")

    # Button to increment turn
    increment_button = tk.Button(
        main_frame,
        text="+1 Turn",
        command=increment_turn,
        font=("Arial", 12),
        bg=button_color,
        fg=bg_color,
    )
    increment_button.grid(row=len(skills) + 1, column=0, pady=10, columnspan=2)

    # Button to decrement turn
    decrement_button = tk.Button(
        main_frame,
        text="-1 Turn",
        command=decrement_turn,
        font=("Arial", 12),
        bg=button_color,
        fg=bg_color,
    )
    decrement_button.grid(row=len(skills) + 2, column=0, pady=1, columnspan=2)

    # Button to edit skills
    edit_button = tk.Button(
        main_frame,
        text="Edit Skills",
        command=open_edit_window,
        font=("Arial", 12),
        bg=button_color,
        fg=bg_color,
    )
    edit_button.grid(row=len(skills) + 3, column=0, pady=1, columnspan=2)
    buff_stacking()
    power_stacking()
    display_magic_levels()


def display_magic_levels():
    global magic_levels
    global MAGICS
    global bonus
    "{'CHAR': 25, 'RADIANT': 55, 'FIRE': 21, 'LIGHT': 53, 'WATER': 6, 'ICE': 6, 'NATURE': 1, 'BLACKSMITH': 21, 'MAGIC SMITH': 10}"
    # Match bonus to magic levels and add them to the magic levels dictionary

    magics_title = tk.Label(
        main_frame,
        text="[Magic Levels]",
        font=("Arial", 12),
        bg=bg_color,
        fg=fg_color,
    )
    magics_title.grid(row=0, column=3, padx=5, pady=1, sticky="w")
    # Reorder the magic levels dictionary to match the order of the MAGICS list
    magic_levels_ = {k: magic_levels[k] for k in MAGICS if k in magic_levels}

    for i, magic in enumerate(magic_levels_):
        if magic.upper() not in MAGICS:
            continue

        magic_var = tk.StringVar(value=f"{magic}: {int(magic_levels_[magic])}")
        magic_label = tk.Label(
            main_frame,
            textvariable=magic_var,
            font=("Arial", 8),
            bg=bg_color,
            fg=fg_color,
        )
        magic_label.grid(row=i + 1, column=3, padx=5, pady=1, sticky="w")


def power_stacking():
    """
    Keeps track of the elements used in the skills and updates the magic levels accordingly
    """
    global magic_levels
    global skills
    global skills_clean
    global bonus
    global MAGICS
    global activated_skills

    # Total damage
    total_damage = 0

    # Dictionary to keep track of the stacked elements
    stacked_elements = {magic: 0 for magic in magic_levels if magic in MAGICS}

    # Title
    stacked_title = tk.Label(
        main_frame,
        text="[Damage]",
        font=("Arial", 12),
        bg=bg_color,
        fg=fg_color,
    )
    stacked_title.grid(row=len(magic_levels), column=3, padx=5, pady=1, sticky="w")

    # Labels
    stacked_vars = {}
    for i, magic in enumerate(magic_levels):
        if magic in MAGICS:
            stacked_var = tk.StringVar(value=f"{magic}: 0")
            stacked_vars[magic] = stacked_var
            stacked_label = tk.Label(
                main_frame,
                textvariable=stacked_var,
                font=("Arial", 8),
                bg=bg_color,
                fg=fg_color,
            )
            stacked_label.grid(
                row=len(magic_levels) + i + 1, column=3, padx=5, pady=1, sticky="w"
            )

    # Check which skills are used
    for skill in skills_clean:
        if skill["turns_left"] > 2:
            # Check if the skill is already activated
            if any(s["name"] == skill["name"] for s in activated_skills):
                continue
            else:
                # Only add skills with a positive duration
                if int(skill["duration"]) > 0:
                    activated_skills.append(
                        {
                            "name": skill["name"],
                            "element": skill["element"],
                            "turns_left": skill["turns_left"],
                            "duration": int(skill["duration"]),
                        }
                    )

    # Stack elements
    for activated_skill in activated_skills:
        element = activated_skill["element"]
        if element in stacked_elements and activated_skill["duration"] > 0:
            stacked_elements[element] += 1

    # Update stacked elements labels
    for element, count in stacked_elements.items():
        if element in stacked_vars:
            stacked_vars[element].set(f"{element}: {count}")

    # Remove expired skills
    activated_skills = [s for s in activated_skills if s["duration"] > 0]

    # Calculate total damage
    for element, count in stacked_elements.items():
        if element in magic_levels:
            total_damage += magic_levels[element] * count

    # Apply weapon bonus if any
    for activated_skill in activated_skills:
        if activated_skill["element"] == "WEAPON":
            # Add char damage to total damage
            total_damage += magic_levels["CHAR"]
            total_damage *= 2

    row_offset = len(magic_levels) + 1
    # Display total damage
    total_damage_var = tk.StringVar(value=f"Total DMG: {total_damage}")
    total_damage_label = tk.Label(
        main_frame,
        textvariable=total_damage_var,
        font=("Arial", 8),
        bg=bg_color,
        fg=fg_color,
    )
    total_damage_label.grid(
        row=row_offset + len(stacked_elements), column=3, padx=5, pady=1, sticky="w"
    )

    # Display activated skills
    # Title
    skill_title = tk.Label(
        main_frame,
        text="[Activated Skills]",
        font=("Arial", 12),
        bg=bg_color,
        fg=fg_color,
    )
    skill_title.grid(
        row=row_offset + len(stacked_elements) + 2, column=3, padx=5, pady=1, sticky="w"
    )

    for i, skill in enumerate(activated_skills):
        skill_var = tk.StringVar(value=f"{skill['name']}")
        skill_label = tk.Label(
            main_frame,
            textvariable=skill_var,
            font=("Arial", 8),
            bg=bg_color,
            fg=fg_color,
        )
        skill_label.grid(
            row=row_offset + len(stacked_elements) + 3 + i,
            column=3,
            padx=5,
            pady=1,
            sticky="w",
        )


def buff_stacking():
    # Keep track of the manually inputed buffs Magic and Damage
    global bonus
    global magic_levels
    global MAGICS
    global skills
    global skills_clean
    global activated_skills

    # Calculate the starting row based on the length of the skills and magic levels
    start_row = len(magic_levels) + 16

    # Label and entry
    buff_title = tk.Label(
        main_frame,
        text="[Buff]",
        font=("Arial", 12),
        bg=bg_color,
        fg=fg_color,
    )
    buff_title.grid(row=start_row, column=3, padx=5, pady=1, sticky="w")

    # Magic
    magic_label = tk.Label(
        main_frame,
        text="Magic Buff:",
        font=("Arial", 8),
        bg=bg_color,
        fg=fg_color,
    )
    magic_label.grid(row=start_row + 1, column=3, padx=5, pady=1, sticky="w")

    magic_entry = tk.Entry(
        main_frame,
        font=("Arial", 8),
        bg=bg_color,
        fg=fg_color,
    )
    magic_entry.grid(row=start_row + 2, column=3, padx=5, pady=1, sticky="w")

    # Damage
    damage_label = tk.Label(
        main_frame,
        text="Damage Buff:",
        font=("Arial", 8),
        bg=bg_color,
        fg=fg_color,
    )
    damage_label.grid(row=start_row + 3, column=3, padx=5, pady=1, sticky="w")

    damage_entry = tk.Entry(
        main_frame,
        font=("Arial", 8),
        bg=bg_color,
        fg=fg_color,
    )
    damage_entry.grid(row=start_row + 4, column=3, padx=5, pady=1, sticky="w")

    # Button to apply the buff
    apply_button = tk.Button(
        main_frame,
        text="Apply",
        command=lambda: apply_buff(magic_entry.get(), damage_entry.get()),
        font=("Arial", 8),
        bg=button_color,
        fg=bg_color,
    )
    apply_button.grid(row=start_row + 5, column=3, padx=5, pady=1, sticky="w")
    reset_button = tk.Button(
        main_frame,
        text="Reset",
        command=lambda: reset_buff(),
        font=("Arial", 8),
        bg=button_color,
        fg=bg_color,
    )
    reset_button.grid(row=start_row + 5, column=3, padx=5, pady=1, sticky="e")


def apply_buff(magic_buff, damage):
    global bonus
    global magic_levels
    global MAGICS

    # Apply magic buff
    if magic_buff:
        for magic in magic_levels:
            magic_levels[magic] += int(magic_buff)

    # Apply damage buff
    if damage:
        magic_levels["CHAR"] += int(damage)

    # Update magic levels
    display_magic_levels()


def reset_buff():
    global bonus
    global magic_levels
    global MAGICS

    # Reset magic levels
    magic_levels = load_magic_levels()

    # Apply bonus to magic levels
    magic_apply_bonus()

    # Update magic levels
    display_magic_levels()


# Function to increment turn and update timers
def increment_turn():
    update_timers()


# Function to decrement turn in case of an error (affects only used skills)
def decrement_turn():
    for skill in skills:
        if skill["turns_left"] < skill["cooldown"] and skill["turns_left"] > 0:
            skill["turns_left"] += 1
    refresh_ui()


# Function to open the edit skills window
def open_edit_window():
    global edit_window, skill_text
    edit_window = tk.Toplevel(root)
    edit_window.title("Edit Skills")
    edit_window.geometry("300x400")
    edit_window.configure(bg=bg_color)

    label = tk.Label(
        edit_window,
        text="Edit Skills (format: name,cooldown):",
        bg=bg_color,
        fg=fg_color,
    )
    label.pack(pady=10)

    skill_text = tk.Text(edit_window, wrap="word", height=15, width=30, bg="lightgray")
    skill_text.pack(pady=10)

    # Populate with current skills in name,cooldown format
    for skill in skills:
        if "[" in skill["name"]:
            skill_text.insert(tk.END, f"{skill['name']}\n")
        elif "-" in skill["name"]:
            skill_text.insert(tk.END, f"{skill['name']}\n")
        elif "{" in skill["name"]:
            skill_text.insert(tk.END, f"{skill['name']}\n")
        else:
            skill_text.insert(
                tk.END, f"{skill['name']},{skill['cooldown']},{skill['element']}\n"
            )

    save_button = tk.Button(
        edit_window,
        text="Save",
        command=save_edited_skills,
        bg=button_color,
        fg=fg_color,
    )
    save_button.pack(pady=1)


# Function to save edited skills from the edit window
def save_edited_skills():
    global skills

    new_skills = skill_text.get("1.0", tk.END).strip().split("\n")
    if not new_skills:
        messagebox.showerror("Error", "Skill list cannot be empty!")
        return

    updated_skills = []
    for line in new_skills:
        parts = line.split(",")
        name = parts[0].strip()
        cooldown = (
            int(parts[1].strip()) if len(parts) > 1 else 3
        )  # Default to cooldown 3 if not provided
        element = parts[2].strip() if len(parts) > 2 else None
        if name:
            # Preserve turns_left if skill already exists
            existing_skill = next((s for s in skills if s["name"] == name), None)
            turns_left = existing_skill["turns_left"] if existing_skill else 0
            updated_skills.append(
                {
                    "name": name,
                    "cooldown": cooldown,
                    "turns_left": turns_left,
                    "element": element,
                }
            )

    # Update the global skill list and refresh the UI
    skills = updated_skills
    save_skills(skills)  # Save to file
    refresh_ui()  # Refresh UI to reflect changes
    edit_window.destroy()  # Close edit window


# Function to load magic levels from a character data file
def load_magic_levels():
    global CHARACTER_NAME
    global bonus
    global magic_levels
    file_path = f"character_data_{CHARACTER_NAME.lower()}.csv"
    if os.path.exists(file_path):
        with open(file_path, mode="r") as file:
            reader = csv.reader(file)
            char_data = list(reader)
            CHARACTER_NAME = char_data[0][0]  # Get the character name from the data
            for row in char_data[2:]:
                magic_levels[row[0]] = int(row[1])

    return magic_levels


def magic_apply_bonus():
    global magic_levels
    global bonus
    for b in bonus:
        if b["element"] in magic_levels:
            magic_levels[b["element"]] += int(b["bonus"])
    display_magic_levels()


# Load magic levels
magic_levels = load_magic_levels()


# Initialize the main window
root = tk.Tk()
root.title("Skill Tracker")
root.configure(bg=bg_color)  # Dark gray background

# Create a frame to hold all the content and make it responsive
main_frame = tk.Frame(root, bg=bg_color)
main_frame.pack(expand=True, fill="both", padx=20, pady=20)

# Configure the grid to expand proportionally
root.grid_rowconfigure(0, weight=1)
root.grid_columnconfigure(0, weight=1)
for i in range(100):
    main_frame.grid_rowconfigure(i, weight=1)
    main_frame.grid_columnconfigure(i, weight=1)
# Load skills from the file
load_skills()

# Apply bonus to magic levels
magic_apply_bonus()

# Apply buff stacking
buff_stacking()

# Start the application loop
root.mainloop()
