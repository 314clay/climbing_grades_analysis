import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Data loading and processing
def v_grade_to_numeric(v_grade):
    if v_grade.startswith('V'):
        try:
            return int(v_grade[1:])
        except ValueError:
            return 0
    return 0

def count_v6_and_harder(climbed_list):
    return sum(1 for grade in climbed_list if v_grade_to_numeric(grade) >= 6)

def calculate_average_difficulty(climbed_list):
    numeric_grades = [v_grade_to_numeric(grade) for grade in climbed_list]
    if numeric_grades:
        return sum(numeric_grades) / len(numeric_grades)
    return 0

def calculate_top_20_average(climbed_list):
    if len(climbed_list) < 20:
        return "N/A"
    numeric_grades = [v_grade_to_numeric(grade) for grade in climbed_list]
    top_20 = sorted(numeric_grades, reverse=True)[:20]
    return sum(top_20) / 20

# Load the climbing data
climbing_data = pd.read_json('climbing_results.json')

# Filter out the first session and keep only Boulder sessions
boulder_data = climbing_data[climbing_data['type'] == 'Boulder'].iloc[1:].reset_index(drop=True)

# Process data for the grid
dates = pd.to_datetime(boulder_data['date']).dt.strftime('%m-%d')
v6_plus_counts = [count_v6_and_harder(session['climbed']) for _, session in boulder_data.iterrows()]
durations = boulder_data['time'].values
calories = boulder_data['cal'].values
total_climbs = [len(session['climbed']) for _, session in boulder_data.iterrows()]
avg_difficulties = [calculate_average_difficulty(session['climbed']) for _, session in boulder_data.iterrows()]
top_20_avgs = [calculate_top_20_average(session['climbed']) for _, session in boulder_data.iterrows()]

# Create the grid visualization
fig, ax = plt.subplots(7, len(dates), figsize=(len(dates)*2, 14))  # Changed to 7 rows
plt.subplots_adjust(hspace=0.4)

# Row 0: Dates
for i, date in enumerate(dates):
    ax[0, i].text(0.5, 0.5, date, ha='center', va='center')
    ax[0, i].axis('off')

# Row 1: V6+ counts
for i, count in enumerate(v6_plus_counts):
    ax[1, i].text(0.5, 0.5, str(count), ha='center', va='center')
    ax[1, i].axis('off')

# Row 2: Duration
for i, duration in enumerate(durations):
    ax[2, i].text(0.5, 0.5, f"{duration}min", ha='center', va='center')
    ax[2, i].axis('off')

# Row 3: Calories
for i, cal in enumerate(calories):
    ax[3, i].text(0.5, 0.5, f"{cal}cal", ha='center', va='center')
    ax[3, i].axis('off')

# Row 4: Total Climbs
for i, total in enumerate(total_climbs):
    ax[4, i].text(0.5, 0.5, str(total), ha='center', va='center')
    ax[4, i].axis('off')

# Row 5: Average Difficulty
for i, avg in enumerate(avg_difficulties):
    ax[5, i].text(0.5, 0.5, f"V{avg:.1f}", ha='center', va='center')
    ax[5, i].axis('off')

# Row 6: Top 20 Average
for i, top_20_avg in enumerate(top_20_avgs):
    if top_20_avg == "N/A":
        ax[6, i].text(0.5, 0.5, "N/A", ha='center', va='center')
    else:
        ax[6, i].text(0.5, 0.5, f"V{top_20_avg:.1f}", ha='center', va='center')
    ax[6, i].axis('off')

# Add row labels on the left
fig.text(0.02, 0.87, 'Date', va='center')
fig.text(0.02, 0.75, 'V6+ Sends', va='center')
fig.text(0.02, 0.63, 'Duration', va='center')
fig.text(0.02, 0.51, 'Calories', va='center')
fig.text(0.02, 0.39, 'Total Sends', va='center')
fig.text(0.02, 0.27, 'Avg Grade', va='center')
fig.text(0.02, 0.15, 'Top 20 Avg', va='center')

plt.show()