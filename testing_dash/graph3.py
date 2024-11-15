import pandas as pd
from dash import dcc, dash_table
import json
from datetime import datetime

def calculate_average_difficulty(climbs):
    grades = [int(climb.replace('V', '')) for climb in climbs]
    return sum(grades) / len(grades) if grades else 0

def count_climbs_above_grade(climbs, threshold):
    return sum(1 for climb in climbs if int(climb.replace('V', '')) >= threshold)

def process_data_for_table(boulder_data, session_ids):
    # Filter for selected sessions
    selected_sessions = boulder_data[boulder_data['session_id'].isin(session_ids)]
    
    table_data = []
    for _, session in selected_sessions.iterrows():
        total_climbs = len(session['climbed'])
        attempts = len(session['attempted'])
        total_tries = total_climbs + attempts
        
        row = {
            'date': pd.to_datetime(session['date']).strftime('%Y-%m-%d'),
            'total_climbs': total_climbs,
            'duration': f"{session['time']} min",
            'calories': session['cal'],
            'failure_rate': f"{(attempts / total_tries * 100):.1f}%" if total_tries > 0 else "0%",
            'avg_grade': f"V{calculate_average_difficulty(session['climbed']):.1f}",
            'v6_plus': count_climbs_above_grade(session['climbed'], 6),
            'v7_plus': count_climbs_above_grade(session['climbed'], 7)
        }
        table_data.append(row)
    
    return table_data

def create_table_figure(data):
    return dash_table.DataTable(
        id='climbing-table',
        columns=[
            {'name': 'Date', 'id': 'date', 'type': 'datetime'},
            {'name': 'Total Climbs', 'id': 'total_climbs', 'type': 'numeric'},
            {'name': 'Duration', 'id': 'duration'},
            {'name': 'Calories', 'id': 'calories', 'type': 'numeric'},
            {'name': 'Failure Rate', 'id': 'failure_rate'},
            {'name': 'Avg Grade', 'id': 'avg_grade'},
            {'name': 'V6+ Climbs', 'id': 'v6_plus', 'type': 'numeric'},
            {'name': 'V7+ Climbs', 'id': 'v7_plus', 'type': 'numeric'}
        ],
        data=data,
        sort_action='native',
        sort_mode='single',
        style_table={
            'height': '400px',
            'overflowY': 'auto',
        },
        style_header={
            'backgroundColor': '#2C2C2C',
            'color': 'white',
            'fontWeight': 'bold',
            'textAlign': 'center',
            'border': '1px solid #404040'
        },
        style_cell={
            'backgroundColor': '#1C1C1C',
            'color': 'white',
            'textAlign': 'center',
            'border': '1px solid #404040',
            'padding': '10px'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': '#262626'
            },
            {
                'if': {'column_id': 'v6_plus', 'filter_query': '{v6_plus} > 0'},
                'backgroundColor': '#2C4F2C',
            },
            {
                'if': {'column_id': 'v7_plus', 'filter_query': '{v7_plus} > 0'},
                'backgroundColor': '#4F2C2C',
            }
        ]
    )

def create_graph3(boulder_data, selected_sessions=None):
    if selected_sessions is None:
        selected_sessions = boulder_data['session_id'].unique()
    
    table_data = process_data_for_table(boulder_data, selected_sessions)
    return create_table_figure(table_data)

# Only for testing
if __name__ == '__main__':
    from dash import Dash
    import html
    
    # Load test data
    with open('climbing_results.json', 'r') as f:
        data = pd.read_json(f)
    
    app = Dash(__name__)
    app.layout = html.Div([
        create_graph3(data)
    ], style={'backgroundColor': '#1C1C1C', 'padding': '20px'})
    
    app.run_server(debug=True)