import tkinter as tk
from tkinter import messagebox
import os

# Define initial skill list
skills = []

# File to store the skills
SKILL_FILE = "skills.csv"

# Define colors
bg_color = "#2C2F33"
button_color = "#262626"
fg_color = "#FFFFFF"


# Function to load skills from a file
def load_skills():
    global skills
    if os.path.exists(SKILL_FILE):
        with open(SKILL_FILE, "r") as file:
            skills = []
            for line in file:
                parts = line.strip().split(",")
                name = parts[0]
                cooldown = (
                    int(parts[1]) if len(parts) > 1 else 3
                )  # Default cooldown is 3
                skills.append({"name": name, "cooldown": cooldown, "turns_left": 0})
    else:
        # Default skills if no file is found
        skills = [
            {"name": "Dual Strike", "cooldown": 3, "turns_left": 0},
            {"name": "Dodge", "cooldown": 3, "turns_left": 0},
            {"name": "Heal", "cooldown": 3, "turns_left": 0},
            {"name": "Holy Sword", "cooldown": 3, "turns_left": 0},
            {"name": "Arrow of Light", "cooldown": 3, "turns_left": 0},
            {"name": "Flash", "cooldown": 3, "turns_left": 0},
            {"name": "Hell Spider", "cooldown": 3, "turns_left": 0},
            {"name": "Purifying Wall", "cooldown": 3, "turns_left": 0},
            {"name": "Divine Slash", "cooldown": 3, "turns_left": 0},
            {"name": "Sunshine Blessing", "cooldown": 3, "turns_left": 0},
            {"name": "Cruel Sun", "cooldown": 3, "turns_left": 0},
            {"name": "Water Ball", "cooldown": 3, "turns_left": 0},
            {"name": "Ice Bow Skill", "cooldown": 3, "turns_left": 0},
        ]
    refresh_ui()


# Function to save skills to a file
def save_skills(skills):
    with open(SKILL_FILE, "w") as file:
        for skill in skills:
            file.write(f"{skill['name']},{skill['cooldown']}\n")


# Function to update the skill timers and refresh the UI
def update_timers():
    for skill in skills:
        if skill["turns_left"] > 0:
            skill["turns_left"] -= 1
    refresh_ui()


# Function to use a skill and start its timer
def use_skill(skill_index):
    skill = skills[skill_index]
    skill["turns_left"] = skill["cooldown"]
    refresh_ui()


# Function to refresh the UI
def refresh_ui():
    # Clear the existing skill label and button widgets if they exist
    for widget in main_frame.winfo_children():
        widget.destroy()

    # Rebuild UI for each skill
    for i, skill in enumerate(skills):
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

        skill_cooldown_label.grid(row=i, column=1, padx=10, pady=5, sticky="w")
        skill_label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

        skill_button = tk.Button(
            main_frame,
            text=f"Use {skill['name']}",
            command=lambda i=i: use_skill(i),
            bg=button_color,
            fg=bg_color,
        )
        skill_button.grid(row=i, column=2, padx=10, pady=5)

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
    decrement_button.grid(row=len(skills) + 2, column=0, pady=5, columnspan=2)

    # Button to edit skills
    edit_button = tk.Button(
        main_frame,
        text="Edit Skills",
        command=open_edit_window,
        font=("Arial", 12),
        bg=button_color,
        fg=bg_color,
    )
    edit_button.grid(row=len(skills) + 3, column=0, pady=5, columnspan=2)


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
        skill_text.insert(tk.END, f"{skill['name']},{skill['cooldown']}\n")

    save_button = tk.Button(
        edit_window,
        text="Save",
        command=save_edited_skills,
        bg=button_color,
        fg=fg_color,
    )
    save_button.pack(pady=5)


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
        if name:
            # Preserve turns_left if skill already exists
            existing_skill = next((s for s in skills if s["name"] == name), None)
            turns_left = existing_skill["turns_left"] if existing_skill else 0
            updated_skills.append(
                {"name": name, "cooldown": cooldown, "turns_left": turns_left}
            )

    # Update the global skill list and refresh the UI
    skills = updated_skills
    save_skills(skills)  # Save to file
    refresh_ui()  # Refresh UI to reflect changes
    edit_window.destroy()  # Close edit window


# Initialize the main window
root = tk.Tk()
root.title("Skill Cooldown Tracker")
root.configure(bg=bg_color)  # Dark gray background

# Create a frame to hold all the content and make it responsive
main_frame = tk.Frame(root, bg=bg_color)
main_frame.pack(expand=True, fill="both", padx=20, pady=20)

# Load skills from the file
load_skills()

# Start the application loop
root.mainloop()
