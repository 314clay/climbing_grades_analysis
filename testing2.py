import dash
from dash import html, dcc
import pandas as pd
from create_session_analysis_figure import create_session_analysis_figure

# Initialize the Dash app
app = dash.Dash(__name__)

# Load and prepare data (similar to the original file)
climbing_data = pd.read_json('climbing_results.json')
boulder_data = climbing_data[climbing_data['type'] == 'Boulder'].iloc[1:].reset_index(drop=True)
boulder_data['session_id'] = range(len(boulder_data))

# Create the figure for sessions 1,2,3,4
selected_sessions = [1, 2, 3, 4]
fig = create_session_analysis_figure(boulder_data, selected_sessions)

# Define the app layout
app.layout = html.Div([
    html.H1('Climbing Session Analysis Dashboard',
            style={'textAlign': 'center', 
                   'color': '#1A5276', 
                   'fontFamily': 'Arial Black',
                   'marginTop': '20px'}),
    
    dcc.Graph(
        id='session-analysis-graph',
        figure=fig,
        style={'margin': 'auto', 'marginTop': '20px'}
    )
], style={'backgroundColor': '#F8F9F9', 'padding': '20px'})

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
