# leaderboard.py
import pandas as pd
import plotly.graph_objects as go
from dash import dcc
from calculate_session_stats import calculate_session_stats

def create_session_leaderboard_figure(boulder_data, session_ids):
    selected_sessions = boulder_data[boulder_data['session_id'].isin(session_ids)]
    if selected_sessions.empty:
        return None
        
    # Create leaderboard data
    leaderboard_data = []
    
    for session_id in session_ids:
        session = boulder_data[boulder_data['session_id'] == session_id]
        if session.empty:
            continue
            
        # Calculate stats for this single session
        result = calculate_session_stats(boulder_data, [session_id])
        if not result:
            continue
            
        stats, completed_climbs, attempted_climbs = result
        
        row_data = {
            'Session Date': session['date'].iloc[0],
            'Duration (min)': float(stats['Session Data']['Average Duration'].replace(' min', '')),
            'Calories': int(stats['Session Data']['Total Calories'].replace(' cal', '')),
            'Avg Difficulty': float(stats['Performance Metrics']['Average Grade'].replace('V', '')) if stats['Performance Metrics']['Average Grade'] != 'N/A' else 0,
            'Number of Climbs': stats['Performance Metrics']['Total Completed'],
            'Failure Rate': float(stats['Performance Metrics']['Failure Rate'].replace('%', ''))
        }
        leaderboard_data.append(row_data)
    
    if not leaderboard_data:
        return None
        
    # Convert to DataFrame for easier sorting
    df = pd.DataFrame(leaderboard_data)
    
    # Create the table figure
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=list(df.columns),
            font=dict(size=14, color='white', family='Arial Black'),
            fill_color='#1A5276',
            align='left',
            height=35,
            line_color='white',
            line_width=1
        ),
        cells=dict(
            values=[df[col] for col in df.columns],
            font=dict(size=12, family='Arial'),
            fill_color=[['#EBF5FB' if i % 2 == 0 else '#D4E6F1' for i in range(len(df))]],
            align='left',
            height=30,
            line_color='white',
            line_width=1,
            format=[
                None,  # Session Date
                '.1f',  # Duration
                'd',   # Calories
                '.1f', # Avg Difficulty
                'd',   # Number of Climbs
                '.1f%' # Failure Rate
            ]
        ),
        columnwidth=[1.5, 1, 1, 1, 1, 1]
    )])
    
    fig.update_layout(
        title=dict(
            text='Session Leaderboard',
            font=dict(size=26, color='#1A5276', family='Arial Black'),
            x=0.5,
            y=0.95
        ),
        height=400,
        width=1200,
        margin=dict(t=100, b=50, l=50, r=50),
        paper_bgcolor='white'
    )
    
    return fig

def create_leaderboard(boulder_data, selected_sessions=None):
    if selected_sessions is None:
        selected_sessions = range(len(boulder_data))
        
    fig = create_session_leaderboard_figure(boulder_data, selected_sessions)
    
    return dcc.Graph(
        id='session-leaderboard',
        figure=fig if fig is not None else {},
        config={'displayModeBar': False}
    )