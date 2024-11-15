
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

def calculate_v_sums_and_averages(climbed_list):
    numeric_grades = [v_grade_to_numeric(grade) for grade in climbed_list]
    if numeric_grades:🟢
 🟢       total_sum = sum(numeric_grades)
        average = total_sum / len(numeric_grades)
    else:
        total_sum = 0
        average = 0
    return total_sum, average

# Load the climbing data
climbing_data = pd.read_json('climbing_results.json')

# Filter out the first session and keep only Boulder sessions
boulder_data = climbing_data[climbing_data['type'] == 'Boulder'].iloc[1:].reset_index(drop=True)

# Define the levels and attempted climbs
v_grades = ['V1', 'V2', 'V3', 'V4', 'V5', 'V6', 'V7', 'V8', 'V9', 'V10']
colors = plt.cm.get_cmap('tab10', len(v_grades)).colors  # Color map for distinct V grades

# Initialize lists to hold data for each session
completed_climbs = {grade: [] for grade in v_grades}
attempted_climbs = {grade: [] for grade in v_grades}

# Process each session
for i, session in boulder_data.iterrows():
    climbed = session['climbed']
    attempted = session['attempted']
    
    # Count climbs and attempts for each V grade
    for grade in v_grades:
        completed_climbs[grade].append(climbed.count(grade))
        attempted_climbs[grade].append(attempted.count(grade))

# Convert to arrays for easier stacking
completed_climbs = {grade: np.array(counts) for grade, counts in completed_climbs.items()}
attempted_climbs = {grade: np.array(counts) for grade, counts in attempted_climbs.items()}

# Lists to hold sums and averages for each session
v_sums = []
v_averages = []

# Calculate for each session
for i, session in boulder_data.iterrows():
    climbed = session['climbed']
    total_sum, avg = calculate_v_sums_and_averages(climbed)
    v_sums.append(total_sum)
    v_averages.append(avg)

# Checking which grades have non-zero values across all sessions for either completed or attempted climbs
non_zero_grades = [grade for grade in v_grades if (completed_climbs[grade].sum() > 0 or attempted_climbs[grade].sum() > 0)]

# Plotting with simplified legend and reverse order
fig, ax = plt.subplots(figsize=(10, 7))
session_indices = np.arange(len(boulder_data))  # X-axis for each session

# Initialize bottom arrays for stacking
bottom_stack = np.zeros(len(boulder_data))

# Reverse the non-zero grades order and plot
for i, grade in enumerate(reversed(non_zero_grades)):  # Reverse the order
    # Plot completed climbs for the current grade
    ax.bar(session_indices, completed_climbs[grade], bottom=bottom_stack, label=f'{grade} completed', color=colors[v_grades.index(grade)])
    bottom_stack += completed_climbs[grade]
    
    # Plot attempted climbs for the current grade
    ax.bar(session_indices, attempted_climbs[grade], bottom=bottom_stack, label=f'{grade} attempted', color=colors[v_grades.index(grade)], alpha=0.5, hatch='//')
    bottom_stack += attempted_climbs[grade]

# Adding the labels for sum and average of V grades above each bar
for i in session_indices:
    ax.text(i, bottom_stack[i] + 0.5, f'Avg: {v_averages[i]:.1f}\nSum: {v_sums[i]}', ha='center', fontsize=10)

# Format the date as MM-DD for each session
dates = pd.to_datetime(boulder_data['date']).dt.strftime('%m-%d')

# Add labels and title
ax.set_xlabel('Bouldering Sessions')
ax.set_ylabel('Number of Climbs')
ax.set_title('Completed and Attempted Bouldering Climbs by Grade (Reversed Order)')
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title="Legend (non-zero only)")
ax.set_xticks(session_indices)
ax.set_xticklabels(dates)

# Set y-axis to hardcode the number of climbs to go up to 35
ax.set_ylim(0, 35)

# Display the plot
plt.tight_layout()
plt.show()
