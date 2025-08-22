import math
import os
import json
from datetime import datetime, timedelta

#--------------STORAGE---------------------------------------------------
LOG_DIR = os.path.join('time_tracker', 'logs')
os.makedirs(LOG_DIR, exist_ok=True)

def load_daily_log(date_str):
    file_path = os.path.join(LOG_DIR, f'{date_str}.json')
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except Exception:
            # Self healing, renames corrupted files
            backup_path = file_path.replace('.json', '_backup.json')
            os.rename(file_path, backup_path)
            print(f"[Warning] Corrupted log detected... Backed up as {backup_path}")
            return {}
    return {}


def save_daily_log(date_str, data):
    os.makedirs(LOG_DIR, exist_ok=True)
    file_path = os.path.join(LOG_DIR, f'{date_str}.json')
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=2)
    print(f"[Saved] Updated log for {date_str}")

def parse_military_time(time_range):
    try:
        start, end = time_range.split('-')
        fmt = '%H%M'
        t1 = datetime.strptime(start, fmt)
        t2 = datetime.strptime(end, fmt)

        if t2 < t1:
            # Assumes time range goes past midnight
            t2 += timedelta(days=1)

        duration = (t2 - t1).total_seconds() / 3600
        # Round to the nearest tenth (1 decimal ish)
        rounded_duration = math.floor(duration * 100 + 0.5) / 100 #round(duration + 1e-8, 1)
        print(f"Raw duration: {duration}, Rounded: {rounded_duration}")

        return rounded_duration
    except Exception:
        raise ValueError("Invalid military time format. Use HHMM-HHMM (ex. 0930-1015). \n")

def add_entry(date_str, charge_code, time_input, comment='', charge_codes=None):
    data = load_daily_log(date_str)
    if charge_codes and charge_code not in charge_codes:
        raise ValueError(f"Invalid charge code. Available: {charge_codes}")


    if charge_code not in data:
        data[charge_code] = []

    hours = parse_military_time(time_input) if '-' in time_input else float(time_input)
    timestamp = datetime.now().isoformat()
    data[charge_code].append({'hours': hours, 'comment': comment, 'timestamp': timestamp})
    save_daily_log(date_str, data)

def undo_last_entry(date_str):
    data = load_daily_log(date_str)
    latest_code = None
    latest_index = -1
    latest_time = None
    
    # Find most recent entry across all charge codes
    for code in data:
        if code == 'charge_codes':
            continue # skip over metadata

        for i in reversed(range(len(data[code]))):
            entry = data[code][i]

            if isinstance(entry, dict):
                ts = entry.get('timestamp', '')
                if not latest_time or ts > latest_time:
                    latest_code = code
                    latest_index = i
                    latest_time = ts

    if latest_code is not None:
        removed = data[latest_code].pop(latest_index)
        save_daily_log(date_str, data)
        return f"Removed last entry from {latest_code}: {removed}."
    else:
        return "No valid entries to undo :( "
    # Remove the latest entry
    #removed = data[latest_code].pop(latest_index)
    #save_daily_log(date_str, data)
    #return f"Removed last entry from {latest_code}: {removed}"
    


def print_daily_summary(date_str):
    data = load_daily_log(date_str)
    if not data:
        print(f"\n--- No entries for {date_str}--- ")
        return

    total_hours_for_day = 0
    
    print(f"\n--- Daily Summary for {date_str} ---")
    for code, entries in data.items():
        if code == 'charge_codes':
            continue #<- skip thru metadata

        # Validate entries are proper dicts with 'hours'
        valid_entries = []
        for e in entries:
            if isinstance(e, dict) and 'hours' in e:
                valid_entries.append(e)
            else:
                print(f"[Warning] Skipping malfunctioning entry under {code}: {e}")


        total = sum(e['hours'] for e in valid_entries)
        total_hours_for_day += total # Add total for this charge code to daily total
        print(f"{code}: {total:.2f} hours")
        for e in valid_entries:
            #desc = f" - {e['hours']}h"
            if e.get('comment'):
                #desc += f": {e['comment']}"
                print(f" - {e['hours']}h: {e['comment']}") 
        
    print(f"\nTotal Number of Hours Worked for {date_str}: {total_hours_for_day:.2f} hours.")

def generate_weekly_summary(start_date):
    summary = {}
    full_week_data = {}
    current = datetime.strptime(start_date, '%Y-%m-%d')
    for _ in range(7):
        date_str = current.strftime('%Y-%m-%d')
        data = load_daily_log(date_str)
        for code, entries in data.items():
            # Skip metadata
            if code == 'charge_codes':
                continue 
            if code not in summary:
                summary[code] = 0
            for entry in entries:
                if isinstance(entry, dict) and 'hours' in entry:
                    summary[code] += entry['hours']
        
        full_week_data[date_str] = data
        current += timedelta(days=1)

    # Save a .txt file name
    weekly_file = os.path.join(LOG_DIR, 'weekly_summary.txt')
    with open(weekly_file, 'w') as f:
        f.write(f"--- Weekly Summary ({start_date}) ---\n")
        for code, total in summary.items():
            f.write(f"{code}: {total:.2f} hours\n")
    print(f"\nWeekly summary saved to {weekly_file}")

    # 
    end_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=0)).strftime('%Y-%m-%d')
    archive_name = f"week_{start_date}_to_{end_date}.json"
    archive_path = os.path.join(LOG_DIR, archive_name)

    with open(archive_path, 'w') as f:
        json.dump(full_week_data, f, indent=2)

    print(f"\nWeekly summary saved to  {weekly_file}...")
    print(f"\nFull weekly archive saved to {archive_path}...Whoop Whoop")
    print(f"Audit me now b****es")


