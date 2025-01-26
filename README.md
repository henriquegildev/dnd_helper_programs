# D&D Helper Programs (Homebrew)

This repository contains a collection of utility programs designed to simplify gameplay for our homebrew Dungeons & Dragons campaign. Whether you’re tracking character levels, managing magic XP, or keeping tabs on skills during combat, these tools are here to make your game smoother and more enjoyable.

### Disclaimer:
This was made for a homebrew campaign, so it might not necessarily work for mainstream D&D.

---

## Available Programs

### **Character Level Tracker -> char_lvl.py**

Welcome to Char Level Calculator 1.0!

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
- **Long Term Tracking/Saving**  
   Save the results instead of having to load data every time.
- **Multiple Magics/Jobs/Skills Tracking**  
   Easily edit the list of magics/jobs.
- **UI Updates**  
   Saving now also updates the UI to display correct magic levels.
- **Multiple Character Support**  
   Switch between characters.
- **Session XP Tracking**  
   Keep track of several XP gains. Session XP is saved and loaded with the character data, unless you reset it.
- **Last Character Load**  
   Program loads the last character used on startup.

#### **Extras**
- **Window Scaling**  
   Scaling of window size of the program is kind of working, but still needs some work.

#### **Todos**
- **Magics/Jobs Linking**  
   Introduce linking where leveling up one magic/job will affect another.
- **Passives Support**  
   Add passive skills that give bonuses to other magics/jobs.
- **Large Number Handling**  
   Ensure the program does not fail for very large numbers.
- **Executable Creation Instructions**  
   Add instructions for executable creation for less technical users/windows users.

#### **How to Use**
1. **Launch the Program**: Open the `char_lvl.py` script to load the XP calculator.
2. **Add Magic Data**: Dynamically create and manage buttons for each spell or skill by editing the provided `character_data.csv` file.
3. **Calculate XP and Level**: Input your current stats, calculate new levels, and save updates with ease.

#### **Requirements**
- Python 3.x
- `tkinter` (built-in with most Python distributions)

---

### **Combat Skill Tracker -> skill_track.py**

Welcome to Skill Tracking 1.0!

A cooldown tracker designed to manage and track the status of skills with cooldowns in a game or similar use case.

#### **Features**
- **Multi Skill Tracking**  
   Track multiple skills simultaneously.
- **Different Cooldowns**  
   Manage skills with varying cooldown periods.
- **Dynamic Skill Editing**  
   Easily edit the list of skills and cooldowns through an intuitive interface.
- **Magic Level Integration**  
   Reads magic levels from character data.
- **Power Stacks and Damage Calculation**  
   Track elements used in skills to calculate power stacks and total damage.
- **Buff Stacking**  
   Manually input magic and damage buffs from other characters, with a reset button included.
- **UI Enhancements**  
   Magic levels and activated skills are now displayed in the UI.
- **Support for Souls and Pets Skills**  
   Added support for tracking skills related to souls and pets.
- **Skill Duration**  
   Skills can now have a duration, affecting the activated skills list and power stacking calculation.
- **Total Damage Calculation**  
   Includes a feature to calculate total damage.
- **Weapon Element**  
   Skills with a Weapon element indicate a doubling attack (e.g., dual strike), which doubles the total damage.

#### **Extras**
- **Bug Fixes**  
   Fixed a bug where the skills were not being saved to the file properly.
- **Window Scaling**  
   Scaling of window size of the program is kind of working, but still needs some work.

#### **Todos**
- **Multiple Characters Support**  
   Add support for managing multiple characters.
- **Fix Scaling Issues**  
   Address and fix window scaling issues.
- **DM Mode**  
   Implement a DM Mode where DMs can load multiple characters or player characters and track their skills usage and damage. (Probably a separate program)
- **Executable Creation Instructions**  
   Add instructions for executable creation for less technical users/windows users.

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
   python3 skill_track.py
   ```

3. Use the application interface to manage skills, cooldowns, and turns.
   - Changes to skills are saved automatically when you click “Save” in the editor.


---

### Enjoy managing your skills without much hassle. And having to do less math, whenever you are leveling Skills, Magics and your Character.

### Enjoy the game! May your rolls always be high, and your campaigns unforgettable.

