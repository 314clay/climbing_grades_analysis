import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def v_grade_to_numeric(v_grade):
   if v_grade.startswith('V'):
       try:
           return int(v_grade[1:])
       except ValueError:
           return 0
   return 0

def calculate_session_stats(boulder_data, session_ids):
   selected_sessions = boulder_data[boulder_data['session_id'].isin(session_ids)]
   
   all_climbs = []
   for _, session in selected_sessions.iterrows():
       all_climbs.extend([v_grade_to_numeric(grade) for grade in session['climbed']])
   
   if not all_climbs:
       return None
   
   v6_plus = len([x for x in all_climbs if x >= 6])
   v6_plus_percentage = round((v6_plus / len(all_climbs)) * 100, 1)
       
   stats = {
       'Performance Metrics': {
           'Total Climbs': len(all_climbs),
           'Average Grade': f"V{round(np.mean(all_climbs), 1)}",
           'Hardest Send': f"V{max(all_climbs)}",
           'Average of Top 20': f"V{round(np.mean(sorted(all_climbs, reverse=True)[:20]), 1)}",
           'V6+ Percentage': f"{v6_plus_percentage}%"
       },
       'Session Data': {
           'Number of Sessions': len(session_ids),
           'Average Climbs/Session': round(len(all_climbs) / len(session_ids), 1),
           'Total Duration': f"{selected_sessions['time'].sum()} min",
           'Average Duration': f"{round(selected_sessions['time'].mean(), 1)} min",
           'Total Calories': f"{selected_sessions['cal'].sum()} cal"
       }
   }
   
   return stats, all_climbs

def create_session_analysis_figure(boulder_data, session_ids):
   # Check if sessions exist
   selected_sessions = boulder_data[boulder_data['session_id'].isin(session_ids)]
   if selected_sessions.empty:
       print("No sessions found for the provided IDs")
       return None
   
   # Get stats and climbs
   stats, all_climbs = calculate_session_stats(boulder_data, session_ids)
   if not stats:
       print("No climbs found for the selected sessions")
       return None

   # Prepare stats for table display
   table_headers = ['Category', 'Metric', 'Value']
   table_cells = [[], [], []]
   
   for category, metrics in stats.items():
       for metric, value in metrics.items():
           table_cells[0].append(category)
           table_cells[1].append(metric)
           table_cells[2].append(value)

   fig = go.Figure()

   # Create color gradient based on grade values
   grade_counts = np.histogram(all_climbs, bins=range(min(all_climbs), max(all_climbs) + 2))[0]
   colors = [f'rgb({int(150-i*10)}, {int(134+i*5)}, {int(193+i*3)})' 
             for i in range(len(grade_counts))]

   # Add histogram
   fig.add_trace(
       go.Histogram(
           x=all_climbs,
           nbinsx=max(all_climbs) - min(all_climbs) + 1,
           name='Climbs',
           xaxis='x',
           yaxis='y',
           marker=dict(
               color=all_climbs,
               colorscale='Viridis',
               line=dict(color='white', width=1)
           ),
           opacity=0.8,
           hovertemplate="Grade: V%{x}<br>Count: %{y}<extra></extra>"
       )
   )

   # Add table
   fig.add_trace(
       go.Table(
           header=dict(
               values=table_headers,
               font=dict(size=14, color='white', family='Arial Black'),
               fill_color='#1A5276',
               align=['left', 'left', 'left'],
               height=35,
               line_color='white',
               line_width=1
           ),
           cells=dict(
               values=table_cells,
               font=dict(size=12, family='Arial'),
               fill_color=[
                   ['#EBF5FB' if i % 2 == 0 else '#D4E6F1' for i in range(len(table_cells[0]))],
                   ['#EBF5FB' if i % 2 == 0 else '#D4E6F1' for i in range(len(table_cells[0]))],
                   ['#EBF5FB' if i % 2 == 0 else '#D4E6F1' for i in range(len(table_cells[0]))]
               ],
               align=['left', 'left', 'left'],
               height=30,
               line_color='white',
               line_width=1
           ),
           domain=dict(x=[0.6, 1], y=[0, 1]),
           columnwidth=[0.3, 0.4, 0.3]
       )
   )

   # Update layout
   fig.update_layout(
       title=dict(
           text='Climbing Session Analysis',
           font=dict(size=26, color='#1A5276', family='Arial Black'),
           x=0.5,
           y=0.95
       ),
       xaxis=dict(
           domain=[0, 0.5],
           title=dict(
               text='V Grade',
               font=dict(size=14, family='Arial Bold')
           ),
           gridcolor='#D5D8DC',
           showgrid=True,
           dtick=1,
           gridwidth=1,
           zeroline=False
       ),
       yaxis=dict(
           title=dict(
               text='Number of Climbs',
               font=dict(size=14, family='Arial Bold')
           ),
           gridcolor='#D5D8DC',
           showgrid=True,
           gridwidth=1,
           zeroline=False
       ),
       height=800,
       width=1200,
       showlegend=False,
       plot_bgcolor='white',
       paper_bgcolor='white',
       margin=dict(t=100, b=50, l=50, r=50)
   )

   # Add background grid lines
   fig.update_xaxes(showline=True, linewidth=1, linecolor='#D5D8DC', mirror=True)
   fig.update_yaxes(showline=True, linewidth=1, linecolor='#D5D8DC', mirror=True)

   return fig

# Example usage:
if __name__ == "__main__":
   # Load and prepare data
   climbing_data = pd.read_json('climbing_results.json')
   boulder_data = climbing_data[climbing_data['type'] == 'Boulder'].iloc[1:].reset_index(drop=True)
   boulder_data['session_id'] = range(len(boulder_data))

   # Create figure
   fig = create_session_analysis_figure(boulder_data, range(len(boulder_data)))
   
   # Show figure if it was created successfully
   if fig is not None:
       fig.show()