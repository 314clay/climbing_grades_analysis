# Adjusting the y-axis to go up to 35 to hardcode the number of climbs

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
ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', title="Legend (non-zero only)")  # Simplified legend
ax.set_xticks(session_indices)
ax.set_xticklabels(dates)  # Set the x-axis labels to session dates in MM-DD format

# Set y-axis to hardcode the number of climbs to go up to 35
ax.set_ylim(0, 35)

# Display the plot
plt.tight_layout()
plt.show()