import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Data loading and preprocessing functions remain the same
def v_grade_to_numeric(v_grade):
   if v_grade.startswith('V'):
       try:
           return int(v_grade[1:])
       except ValueError:
           return 0
   return 0

# Load and process data
climbing_data = pd.read_json('climbing_results.json')
boulder_data = climbing_data[climbing_data['type'] == 'Boulder'].iloc[1:].reset_index(drop=True)

# Create figure with secondary y-axis
fig = make_subplots(rows=2, cols=1, 
                   vertical_spacing=0.2,
                   subplot_titles=('Session Timeline', 'Grade Distribution'))

# Add scatter plot to first subplot
fig.add_trace(
   go.Scatter(x=boulder_data['date'], 
              y=[1]*len(boulder_data),  # All dots on same level
              mode='markers',
              marker=dict(size=12),
              customdata=boulder_data.index,  # Store index for click event
              hovertemplate='Date: %{x}<extra></extra>'),
   row=1, col=1
)

# Add dummy histogram to second subplot (initially hidden)
fig.add_trace(
   go.Histogram(x=[0,1,1,2,2,2,3,3,4], 
                visible=False,
                name='Grade Distribution'),
   row=2, col=1
)

# Update layout
fig.update_layout(
   title='Boulder Sessions',
   showlegend=False,
   height=700
)

# Add click event callback
fig.update_layout(
   clickmode='event+select'
)

# Hide y-axis for timeline
fig.update_yaxes(showticklabels=False, row=1, col=1)

# Add this JavaScript callback for click events
fig.update_layout(
   updatemenus=[
       dict(
           type='buttons',
           showactive=False,
           buttons=[
               dict(
                   label='Reset View',
                   method='update',
                   args=[{'visible': [True, False]}]  # Show timeline, hide histogram
               )
           ]
       )
   ]
)

fig.show()