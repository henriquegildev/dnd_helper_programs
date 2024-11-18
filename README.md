# D&D Helper Programs (Homebrew)

This repository contains a collection of utility programs designed to simplify gameplay for our homebrew Dungeons & Dragons campaign. Whether you’re tracking character levels, managing magic XP, or keeping tabs on skills during combat, these tools are here to make your game smoother and more enjoyable.

### Disclaimer:
This was made for a homebrew campaign, so it might not necessarily work for mainstream D&D.

---

## Available Programs

### **Character Level tracker -> char_lvl.py**

A D&D XP Calculator and character manager tailored for campaigns using a homebrew leveling system where XP required is calculated as **10 × next level**.

#### **Features**
- **Dynamic Level Calculation**  
    Input current XP, level, and XP gained to instantly compute the new level and remaining XP.
- **Magic Management**  
    Manage a list of spells or skills (referred to as "magics"), including their levels, current XP, and required XP for the next level.
- **Custom Multiplier Support**  
    Switch between multipliers of 1, 10, 100, and 1000 to adapt the program to different progression systems.
- **Data Editing**  
    View and edit magic data directly through an intuitive interface that reads from and writes to a CSV file.
- **User-Friendly UI**  
    Features buttons for quick actions like resetting fields, editing character data, or saving updates.
##### TODO
- **Easy Multi-character support**: Switch between characters with a click. Adding them by having multiple csv files (maybe).
- **Display character names**: Easy to see name and titles.

#### **How to Use**
1. **Launch the Program**: Open the `char_lvl.py` script to load the XP calculator.
2. **Add Magic Data**: Dynamically create and manage buttons for each spell or skill by editing the provided `character_data.csv` file.
3. **Calculate XP and Level**: Input your current stats, calculate new levels, and save updates with ease.

#### **Requirements**
- Python 3.x
- `tkinter` (built-in with most Python distributions)

---

### **Combat Skill Tracker -> skill_track.py**

A cooldown tracker designed to manage and track the status of skills with cooldowns in a game or similar use case.

#### **Features**
-  **Cooldown Management**  
   Users can activate skills, which then start a cooldown timer. The timer automatically decrements each turn.
-  **Manual Turn Adjustment**  
   Options to increment or decrement turns in case of errors or turn-based gameplay adjustments.
-  **Dynamic Skill Editing**  
   Modify, add, or remove skills through an easy-to-use editing window. Skill changes can be saved to a CSV file for future sessions.
-  **Persistent Skill Data**  
   The skill list is saved to a CSV file (`skills.csv`), allowing the application to retain user preferences between runs.
-  **Customizable Design**  
   The application uses a clean, dark-themed UI with configurable colors.

#### **Getting Started**

##### **Requirements**
- Python 3.x
- No additional libraries required; the application uses only the standard library.

##### **Installation**
1. Clone or download this repository to your machine.
2. Ensure Python 3.x is installed on your system.

##### **Running the Application**
1. Save the `skill_track.py` file in a directory.
2. Open a terminal or command prompt and navigate to the directory.
3. Run the script using:
   ```bash
   python skill_track.py

---

### **Usage Guide**

#### **Main Screen**
1. **Skill Buttons**  
   - Each skill has a button labeled **"Use [Skill Name]"** to activate it.  
   - If a skill is on cooldown, its button is disabled, and the remaining cooldown turns are displayed next to the skill's name.
2. **Turn Management**  
   - Use the `+1 Turn` button to advance turns, which automatically decrements cooldown timers for all active skills.  
   - Use the `-1 Turn` button to reverse turns in case of errors, restoring one turn to all currently cooling down skills.
3. **Edit Skills**  
   - Click the **"Edit Skills"** button to open an editor window, where you can dynamically add, modify, or remove skills and their cooldowns.

#### **Editing Skills**
- In the editor window, skills are listed in the format:  

skill_name,cooldown

- Example:  
```
Dual Strike,3
Heal,2
New Skill,4
```
- After editing, click **"Save"** to update the skill list and apply changes immediately.

#### **Customizing Colors**
- The application's color scheme is defined within the script:  
- **Background Color**: `bg_color = "#2C2F33"`  
- **Button Color**: `button_color = "#262626"`  
- **Text Color**: `fg_color = "#FFFFFF"`  

You can modify these variables at the top of the `skill_track.py` script to match your preferences.

#### **Default Skills**
If `skills.csv` does not exist, the program initializes with these default skills (each with a cooldown of 3 turns):  
- Dual Strike  
- Dodge  
- Heal  
- Holy Sword  
- Arrow of Light  
- Flash  
- Hell Spider  
- Purifying Wall  
- Divine Slash  
- Sunshine Blessing  
- Cruel Sun  
- Water Ball  
- Ice Bow Skill  

#### **Saving and Loading Data**
- The program saves skill data to `skills.csv`.  
- On startup, it loads skill data from this file if it exists.  
- If no file is found, the application generates a new `skills.csv` with the default skills.

#### **Running the Application**
1. Save the `skill_track.py` file in a directory.
2. Open a terminal or command prompt, navigate to the directory, and run:
 ```bash
   python skill_track.py
```

3.	Use the application interface to manage skills, cooldowns, and turns.
  - Changes to skills are saved automatically when you click “Save” in the editor.

---

### Enjoy managing your skills without much hassle. And having to do less math, whenever you are leveling Skills, Magics and your Character.

### Enjoy the game! May your rolls always be high, and your campaigns unforgettable.

