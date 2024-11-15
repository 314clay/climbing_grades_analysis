from dash import Dash, html
from dash.dependencies import Input, Output
from graph1 import create_graph1
from graph2 import create_graph2, create_session_analysis_figure
import pandas as pd

app = Dash(__name__)

# Load data once at startup
climbing_data = pd.read_json('climbing_results.json')
boulder_data = climbing_data[climbing_data['type'] == 'Boulder'].iloc[1:].reset_index(drop=True)
boulder_data['session_id'] = range(len(boulder_data))

app.layout = html.Div([
    create_graph1(),
    create_graph2(boulder_data)
])

@app.callback(
    Output('session-analysis-graph', 'figure'),
    [Input('timeline-graph', 'selectedData'),
     Input('timeline-graph', 'clickData')]  # Added clickData
)
def update_session_analysis(selected_data, click_data):
    if selected_data:
        # Get indices of selected points
        selected_indices = [point['pointIndex'] for point in selected_data['points']]
        print(f"Selected indices: {selected_indices}")  # Debug print
        return create_session_analysis_figure(boulder_data, selected_indices)
    elif click_data:
        # Handle single click
        index = click_data['points'][0]['pointIndex']
        print(f"Clicked index: {index}")  # Debug print
        return create_session_analysis_figure(boulder_data, [index])
    else:
        # Default to showing all sessions
        print("No selection, showing all")  # Debug print
        return create_session_analysis_figure(boulder_data, range(len(boulder_data)))

if __name__ == '__main__':
    app.run_server(debug=True)