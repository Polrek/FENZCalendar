##Polrek
##Generates the shift calendar for FENZ for 2025 onwards

####TODO:
##fix the leave group pattern so it's not hard coded
##output a json file
##multi-year support

import json
from datetime import datetime, timedelta

# Define the start date and the leave group pattern
start_date = datetime(2024, 10, 8)  # 08 Oct 2024
leave_group_pattern = [ #TODO: better way to do this?
    1, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    2, 0, 2, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    3, 0, 3, 0, 3, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    4, 0, 4, 0, 4, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    5, 0, 5, 0, 5, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    6, 0, 6, 0, 6, 0, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    7, 0, 7, 0, 7, 0, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    8, 0, 8, 0, 8, 0, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    9, 0, 9, 0, 9, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    10, 0, 10, 0, 10, 0, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0
]

# Function to calculate the leave group based on the pattern and date
def get_leave_group(date):
    days_since_start = (date - start_date).days
    pattern_index = days_since_start % len(leave_group_pattern)
    return leave_group_pattern[pattern_index]

# Define the watch cycle starting from 08 Oct 2024
watch_cycle = [
    ('Green', 'Blue'),  # DayShift: Green, NightShift: Blue
    ('Green', 'Blue'),
    ('Red', 'Green'),
    ('Red', 'Green'),
    ('Brown', 'Red'),
    ('Brown', 'Red'),
    ('Blue', 'Brown'),
    ('Blue', 'Brown')
]

# Generate the shifts for 2025
shifts_by_month = []
current_date = datetime(2025, 1, 1)  # Start from January 2025

# Loop through all days in 2025
while current_date.year == 2025:
    # Get the corresponding leave group for the current date
    leave_group = get_leave_group(current_date)
    
    # Determine the day and night shift watch based on the cycle
    day_shift_watch, night_shift_watch = watch_cycle[(current_date - start_date).days % len(watch_cycle)]

    # Create the day shift and night shift data
    day_shift = {
        "Watch": day_shift_watch,
        "StartTime": current_date.strftime("%Y-%m-%dT08:00:00"),
        "EndTime": (current_date + timedelta(hours=10)).strftime("%Y-%m-%dT18:00:00"),
        "ShiftDate": current_date.strftime("%Y-%m-%d")
    }
    
    night_shift = {
        "Watch": night_shift_watch,
        "StartTime": (current_date + timedelta(hours=10)).strftime("%Y-%m-%dT18:00:00"),
        "EndTime": (current_date + timedelta(hours=22)).strftime("%Y-%m-%dT08:00:00"),
        "ShiftDate": current_date.strftime("%Y-%m-%d")
    }

    day_data = {
        "Date": current_date.strftime("%Y-%m-%dT00:00:00"),
        "DayShift": day_shift,
        "NightShift": night_shift,
        "LeaveGroup": leave_group
    }

    # Check if the current date is the start of a new month
    current_month = current_date.month
    month_data = next((month for month in shifts_by_month if month['Month'] == current_month), None)
    
    if not month_data:
        month_data = {
            "Year": current_date.year,
            "Month": current_month,
            "Name": current_date.strftime("%B"),  # Get full month name (January, February, etc.)
            "Days": []
        }
        shifts_by_month.append(month_data)
    
    month_data["Days"].append(day_data)

    # Move to the next day
    current_date += timedelta(days=1)

# Print the result in JSON format
print(json.dumps(shifts_by_month, indent=2))
