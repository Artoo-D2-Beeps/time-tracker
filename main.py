from tracker import *
from datetime import datetime
import sys
import os
import json

#debug
print("Starting script...")
#  Interactive runner?

LOG_DIR = os.path.join('time_tracker', 'logs')

def load_existing_charge_codes(today):
    log_path = os.path.join(LOG_DIR, f"{today}.json")
    if os.path.exists(log_path):
        try:
            with open(log_path, 'r') as file:
                data = json.load(file)
                codes = data.get('charge_codes')
                if isinstance(codes, list) and all(isinstance(c, str) for c in codes):
                    print(f"Loaded charge codes from today's log: {', '.join(codes)}")
                    return codes
                else:
                    raise ValueError("charge_codes malfunction hehe or missing...")
        except Exception as e:
            #Adding self healing, backup and resets
            backup_path = log_path.replace('.json', '_backup.json')
            os.rename(log_path, backup_path)
            print(f"Corrupted log detected. Backed up as {backup_path}...")
            print("Starting fresh log for today :)\n")
            # print(f"Failed to load existing charge codes: {e}...")
    return []


def run():
    today = datetime.now().strftime('%Y-%m-%d')
    charge_codes = load_existing_charge_codes(today)

    if not charge_codes:
        print("Enter up to 6 charge codes for today. ")
        print("Type 'quit' anytime to exit before starting.\n")
        for i in range(6):
            code = input(f"Enter charge code {i+1} (or leave blank): ").strip()
            if code.lower() == 'quit':
                print("")
                sys.exit() #or quit might be safer
            if code:
                charge_codes.append(code)
        
        
        if not charge_codes:
            print("No charge codes entered. Exiting...")
            return
        
        # Save only if we crfeated new charge codes
        save_daily_log(today, {'charge_codes': charge_codes})
        print(f"[DEBUG] New charge codes saved for {today}")
    
    
    while True:
        print("\nOptions: [add] entry, [summary] today, [weekly] summary, [undo], [addcode], [quit]")
        choice = input("Select option: ").strip().lower()

        if choice == 'add':
            while True:
                code = input(f"Enter charge code ({', '.join(charge_codes)})\n (To go back to main menu, press cancel): ").strip()
                if code.lower() == 'cancel':
                    break
                if code not in charge_codes:
                    print("Invalid charge code. Try again.\n")
                    continue

                time_input = input("Enter time (e.g., 1230-1300 or 1.5): ").strip()
                if '-' in time_input:
                    try:
                        _ = int(time_input.split('-')[0])
                        _ = int(time_input.split('-')[1])
                    except ValueError:
                        print("Invalid military time format. Try again (ex. 1230-1315). \n")
                        continue
                else:
                    try:
                        _ = float(time_input)
                    except ValueError:
                        print("Invalid hour format, try again (HHMM): \n")
                        continue

                comment = input("Optional comment: ").strip()
                try:
                    add_entry(today, code, time_input, comment, charge_codes)
                    print("Entry added.")
                    
                except Exception as e:
                    print(f"Something went wrong: {e}")
                break # <- This changed from continue to only exit after successful add...

        elif choice == 'summary':
            print_daily_summary(today)

        elif choice == 'weekly':
            start_date = input("Enter week start date (YYYY-MM-DD): ").strip()
            generate_weekly_summary(start_date)

        elif choice == 'undo':
            result = undo_last_entry(today)
            print(result)
        elif choice == 'addcode':
            new_code = input("Enter a new charge code to add: ").strip()
            if new_code in charge_codes:
                print(f" '{new_code} already exists.")
            elif new_code:
                charge_codes.append(new_code)
                # Update new log file immediately
                log_path = os.path.join(LOG_DIR, f"{today}.json")
                try:
                    with open(log_path, 'r+') as file:
                        data = json.load(file)
                        data['charge_codes'] = charge_codes
                        file.seek(0)
                        json.dump(data, file, indent=2)
                        file.truncate()
                    print(f"Added '{new_code}' to today's charge codes...")
                except Exception as e:
                    print(f"Failed to update log file: {e}")

        elif choice == 'quit':
            print("Goodbye :)\n")
            break

        else:
            print("Invalid option.")

if __name__ == '__main__':
    run()
