import pandas as pd
import plotly.graph_objects as go
from dash import dcc
from utils import calculate_average_difficulty

def process_climbing_data(data_path):
    climbing_data = pd.read_json(data_path)
    boulder_data = climbing_data[climbing_data['type'] == 'Boulder'].iloc[1:].reset_index(drop=True)
    
    dates = pd.to_datetime(boulder_data['date'])
    total_climbs = [len(session['climbed']) for _, session in boulder_data.iterrows()]
    avg_difficulties = [calculate_average_difficulty(session['climbed']) 
                       for _, session in boulder_data.iterrows()]
    
    return dates, total_climbs, avg_difficulties

def create_timeline_figure(dates, total_climbs, avg_difficulties):
    fig = go.Figure()
    
    # Add timeline line
    fig.add_trace(go.Scatter(
        x=dates,
        y=[0] * len(dates),
        mode='lines',
        line=dict(color='#404040', width=2),
        hoverinfo='skip'
    ))
    
    # Add scatter points
    fig.add_trace(go.Scatter(
        x=dates,
        y=[0] * len(dates),
        mode='markers+text',
        marker=dict(
            size=[count * 5 for count in total_climbs],
            color=avg_difficulties,
            colorscale='Magma',
            line=dict(color='white', width=1),
            colorbar=dict(
                title='Average V-Grade',
                titleside='right',
                titlefont=dict(color='white'),
                tickfont=dict(color='white')
            )
        ),
        text=[f"{count} climbs<br>Avg: V{avg:.1f}" 
              for count, avg in zip(total_climbs, avg_difficulties)],
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
        height=600,
        # Add dragmode for selection
        dragmode='select'
    )
    
    return fig

def create_graph1(data_path='climbing_results.json'):
    dates, total_climbs, avg_difficulties = process_climbing_data(data_path)
    fig = create_timeline_figure(dates, total_climbs, avg_difficulties)
    return dcc.Graph(
        id='timeline-graph',
        figure=fig,
        config={
            'displayModeBar': True,
            'modeBarButtonsToAdd': ['select2d', 'lasso2d'],
            'scrollZoom': True
        },
        # Enable selection modes
        clear_on_unhover=False,
        selectedData=None,
        clickData=None
    )