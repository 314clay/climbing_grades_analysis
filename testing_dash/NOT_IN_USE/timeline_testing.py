import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

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

# Load the climbing data
climbing_data = pd.read_json('climbing_results.json')

# Filter out the first session and keep only Boulder sessions
boulder_data = climbing_data[climbing_data['type'] == 'Boulder'].iloc[1:].reset_index(drop=True)

# Process data
dates = pd.to_datetime(boulder_data['date'])
total_climbs = [len(session['climbed']) for _, session in boulder_data.iterrows()]
avg_difficulties = [calculate_average_difficulty(session['climbed']) for _, session in boulder_data.iterrows()]

# Create the timeline visualization
fig = go.Figure()

# Add the timeline line
fig.add_trace(go.Scatter(
    x=dates,
    y=[0] * len(dates),
    mode='lines',
    line=dict(color='#404040', width=2),
    hoverinfo='skip'
))

# Add the scatter points with much smaller circles
fig.add_trace(go.Scatter(
    x=dates,
    y=[0] * len(dates),
    mode='markers+text',
    marker=dict(
        size=[count * 5 for count in total_climbs],  # Significantly reduced size multiplier
        color=avg_difficulties,
        colorscale='Magma',
        line=dict(color='white', width=1),  # Reduced border width
        colorbar=dict(
            title='Average V-Grade',
            titleside='right',
            titlefont=dict(color='white'),
            tickfont=dict(color='white')
        )
    ),
    text=[f"{count} climbs<br>Avg: V{avg:.1f}" for count, avg in zip(total_climbs, avg_difficulties)],
    textposition="top center",
    textfont=dict(color='white', size=12),
    hoverinfo='text',
    hovertext=[f"Date: {date.strftime('%m-%d')}<br>Climbs: {count}<br>Avg Grade: V{avg:.1f}" 
               for date, count, avg in zip(dates, total_climbs, avg_difficulties)]
))

# Update layout
fig.update_layout(
    plot_bgcolor='#1C1C1C',
    paper_bgcolor='#1C1C1C',
    title=dict(
        text='Climbing Progress Timeline',
        font=dict(size=24, color='white'),
        x=0.5,
        y=0.95
    ),
    showlegend=False,
    xaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=True,
        tickfont=dict(color='white'),
        tickangle=45
    ),
    yaxis=dict(
        showgrid=False,
        zeroline=False,
        showline=False,
        showticklabels=False,
        range=[-0.5, 0.5]
    ),
    margin=dict(l=50, r=50, t=100, b=50),
    height=600
)

# Show the figure
fig.show()