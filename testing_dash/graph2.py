# graph2.py
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from dash import dcc
from calculate_session_stats import calculate_session_stats

def v_grade_to_numeric(v_grade):
   if v_grade.startswith('V'):
       try:
           return int(v_grade[1:])
       except ValueError:
           return 0
   return 0


def create_session_analysis_figure(boulder_data, session_ids):
   selected_sessions = boulder_data[boulder_data['session_id'].isin(session_ids)]
   if selected_sessions.empty:
       return None
   
   result = calculate_session_stats(boulder_data, session_ids)
   if not result:
       return None
       
   stats, completed_climbs, attempted_climbs = result

   table_headers = ['Category', 'Metric', 'Value']
   table_cells = [[], [], []]
   
   for category, metrics in stats.items():
       for metric, value in metrics.items():
           table_cells[0].append(category)
           table_cells[1].append(metric)
           table_cells[2].append(value)

   fig = go.Figure()

   # Add histogram for completed climbs
   max_grade = max(max(completed_climbs or [0]), max(attempted_climbs or [0]))
   min_grade = min(min(completed_climbs or [0]), min(attempted_climbs or [0]))
   
   fig.add_trace(
       go.Histogram(
           x=completed_climbs,
           nbinsx=max_grade - min_grade + 1,
           name='Completed',
           xaxis='x',
           yaxis='y',
           marker=dict(
               color='#1A5276',
               line=dict(color='white', width=1)
           ),
           opacity=0.8,
           hovertemplate="Grade: V%{x}<br>Completed: %{y}<extra></extra>"
       )
   )

   # Add histogram for attempted climbs
   fig.add_trace(
       go.Histogram(
           x=attempted_climbs,
           nbinsx=max_grade - min_grade + 1,
           name='Attempted',
           xaxis='x',
           yaxis='y',
           marker=dict(
               color='orange',
               line=dict(color='white', width=1)
           ),
           opacity=0.8,
           hovertemplate="Grade: V%{x}<br>Attempted: %{y}<extra></extra>"
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

   fig.update_layout(
       barmode='stack',
       title=dict(
           text='Climbing Session Analysis',
           font=dict(size=26, color='#1A5276', family='Arial Black'),
           x=0.5,
           y=0.95
       ),
       xaxis=dict(
           domain=[0, 0.5],
           title=dict(text='V Grade', font=dict(size=14, family='Arial Bold')),
           gridcolor='#D5D8DC',
           showgrid=True,
           dtick=1,
           gridwidth=1,
           zeroline=False
       ),
       yaxis=dict(
           title=dict(text='Number of Climbs', font=dict(size=14, family='Arial Bold')),
           gridcolor='#D5D8DC',
           showgrid=True,
           gridwidth=1,
           zeroline=False
       ),
       height=800,
       width=1200,
       showlegend=True,
       legend=dict(
           x=0.02,
           y=0.98,
           bgcolor='rgba(255, 255, 255, 0.8)',
           bordercolor='#D5D8DC'
       ),
       plot_bgcolor='white',
       paper_bgcolor='white',
       margin=dict(t=100, b=50, l=50, r=50)
   )

   fig.update_xaxes(showline=True, linewidth=1, linecolor='#D5D8DC', mirror=True)
   fig.update_yaxes(showline=True, linewidth=1, linecolor='#D5D8DC', mirror=True)

   return fig

def create_graph2(boulder_data, selected_sessions=None):
   if selected_sessions is None:
       selected_sessions = range(len(boulder_data))
       
   fig = create_session_analysis_figure(boulder_data, selected_sessions)
   
   return dcc.Graph(
       id='session-analysis-graph',
       figure=fig if fig is not None else {},
       config={'displayModeBar': False}
   )