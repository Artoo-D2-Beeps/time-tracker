# ⏱️ Time Tracker CLI Tool

A simple yet powerful command-line tool to track work hours using charge codes. Built in Python with a focus on clean logs, flexible time input, and self-healing storage.

Fun Symbols 🎨 below used from https://coolsymbol.com/
---

## 🚀 Features

- Track time per task using custom charge codes
- Accepts military time ranges (`HHMM-HHMM`) or decimal hours (`1.5`)
- Undo last time entry
- View daily or weekly summaries
- Saves daily logs in JSON
- Automatically backs up corrupted logs

---

## 🤝 Project Structure

time-tracker/
├── main.py # Command-line interface
├── tracker/
│ ├── init.py
│ └── tracker.py # Core logic
├── time_tracker/logs/ # Auto-created logs (not committed)
├── .gitignore
└── README.md

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/YOUR_USERNAME/time-tracker.git
cd time-tracker

### 2. Run the App

python main.py

You'll be prompted to enter six charge codes, then start tracking time. Feel free to change the 
number of charge codes you want or need. If you have less, enter however many you have then
press 'ENTER' to skip through. I felt six was enough but not too much :)

See bottom of README for warnings.

--------------------------------------------------------------------------------------------------------------
### Usage Example 

Enter up to 6 charge codes for today.
Enter charge code 1 (or leave blank): DEV
Enter charge code 2 (or leave blank): MEETING
...

Options: [add] entry, [summary] today, [weekly] summary, [undo], [addcode], [quit]
Select option: add

Enter charge code (DEV, MEETING): DEV
Enter time (e.g., 1230-1300 or 1.5): 0930-1130
Optional comment: Refactoring modules
Entry added.

------------------------------------------------------------------------------------------------------------------

⚒️ Tech Stack
Python 3.x
No external libraries (100% standard library)

🕶 Future Plans
Export logs to CSV
Web dashboard (Flask or FastAPI)
Config file for recurring charge codes

📖 Author
Made with Beeps and Bops by Artoo
GitHub Profile

🧾 License
This project is licensed under the MIT License.

---

## 🔚 Final Notes

WARNING: When you type [summary] to get weekly summary, the output is not work appropriate. Change
if you are showing this to your manage. It's mainly for me to feel any semblence of control if I ever get audited.

WARNING: 
Save weekly document...weekly as a different name. I have folders for each month and do it that way. If you
don't, the next week will override the last document.

May the force be with you. 🤖