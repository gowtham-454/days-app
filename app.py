from flask import Flask, render_template, request, jsonify
import datetime
import calendar
import json
import os

app = Flask(__name__)

# File to store checked days
DATA_FILE = 'checked_days.json'

# Load checked days from the JSON file
def load_checked_days():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    return {}

# Save checked days to the JSON file
def save_checked_days(checked_days):
    with open(DATA_FILE, 'w') as f:
        json.dump(checked_days, f)

# Initialize checked_days from the JSON file
checked_days = load_checked_days()

@app.route('/')
def index():
    today = datetime.datetime.now()
    return render_template('index.html', today=today)

@app.route('/toggle_day', methods=['POST'])
def toggle_day():
    day = request.json.get('day')
    month = request.json.get('month')
    state = request.json.get('state')  # Get the state from the request

    # Create a unique key for each day
    key = f"{month}-{day}"
    
    # Update the checked_days dictionary with the new state
    checked_days[key] = state
    
    # Save changes to the JSON file
    save_checked_days(checked_days)

    return jsonify(checked_days)

@app.route('/get_month', methods=['POST'])
def get_month():
    month = request.json.get('month')
    year = request.json.get('year')
    
    # Get the name of the month
    month_name = calendar.month_name[month]

    # Generate the calendar for the given month and year
    month_calendar = calendar.monthcalendar(year, month)

    return jsonify({
        'month_name': month_name,
        'year': year,
        'month_calendar': month_calendar,
        'checked_days': checked_days  # Return current states of days
    })

@app.route('/get_streaks', methods=['POST'])
def get_streaks():
    current_streak = 0
    longest_checked_streak = 0
    longest_unchecked_streak = 0

    # Get today's date
    today = datetime.datetime.now()
    
    # Iterate through all stored days to calculate streaks, starting from September (month 9)
    days_list = sorted(checked_days.keys(), key=lambda x: (int(x.split('-')[0]), int(x.split('-')[1])))  # Sort by month and day

    temp_checked_streak = 0
    temp_unchecked_streak = 0
    
    last_checked_date = None  # To track last checked date for current streak

    for key in days_list:
        month, day_str = map(int, key.split('-'))
        day = int(day_str)
        
        # Only consider dates from September onward
        if month < 9:
            continue
        
        # Check if this day is in the past or present
        date_to_check = datetime.datetime(today.year, month, day)
        
        if date_to_check > today:
            continue  # Skip future dates

        if checked_days[key] == "checked":
            temp_checked_streak += 1
            temp_unchecked_streak = 0
            
            longest_checked_streak = max(longest_checked_streak, temp_checked_streak)
            
            last_checked_date = date_to_check
            
            # Check if yesterday was also checked
            yesterday_date = date_to_check - datetime.timedelta(days=1)
            yesterday_key = f"{yesterday_date.month}-{yesterday_date.day}"
            if yesterday_key in checked_days and checked_days[yesterday_key] == "unchecked":
                current_streak += 1  # Only count as a new streak if today is checked and yesterday was unchecked
                
            elif yesterday_key in checked_days and checked_days[yesterday_key] == "checked":
                current_streak += 1 if last_checked_date else 0
            
        elif checked_days[key] == "unchecked":
            temp_unchecked_streak += 1
            temp_checked_streak = 0
            
            longest_unchecked_streak = max(longest_unchecked_streak, temp_unchecked_streak);
            
            # Reset current streak if yesterday was unchecked
            yesterday_date = date_to_check - datetime.timedelta(days=1)
            yesterday_key = f"{yesterday_date.month}-{yesterday_date.day}"
            if yesterday_key in checked_days and checked_days[yesterday_key] == "unchecked":
                current_streak = 0
        
        else:
            current_streak += (temp_checked_streak + temp_unchecked_streak) 

    return jsonify({
        'current_streak': current_streak,
        'longest_checked_streak': longest_checked_streak,
        'longest_unchecked_streak': longest_unchecked_streak,
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)  # Bind to all interfaces