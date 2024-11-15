from utils import v_grade_to_numeric
import numpy as np

def calculate_session_average(climbs):
    # Filter out grades <= 3
    filtered_climbs = [grade for grade in climbs if grade > 3]
    if not filtered_climbs:
        return None
        
    if len(climbs) <= 20:
        # If 20 or fewer climbs, take average of all climbs > 3
        return np.mean(filtered_climbs)
    else:
        # If more than 20 climbs, take average of top 20
        return np.mean(sorted(climbs, reverse=True)[:20])

def calculate_session_stats(boulder_data, session_ids):
    selected_sessions = boulder_data[boulder_data['session_id'].isin(session_ids)]
    
    completed_climbs = []
    attempted_climbs = []
    for _, session in selected_sessions.iterrows():
        completed_climbs.extend([v_grade_to_numeric(grade) for grade in session['climbed']])
        attempted_climbs.extend([v_grade_to_numeric(grade) for grade in session['attempted']])
    
    all_climbs = completed_climbs + attempted_climbs
    
    if not all_climbs:
        return None
        
    # Calculate failure rate
    total_attempts = len(attempted_climbs)
    total_completed = len(completed_climbs)
    failure_rate = round((total_attempts / (total_completed + total_attempts) * 100), 1) if (total_completed + total_attempts) > 0 else 0
    
    v6_plus = len([x for x in completed_climbs if x >= 6])
    v6_plus_percentage = round((v6_plus / len(completed_climbs)) * 100, 1) if completed_climbs else 0
    
    # Calculate session averages
    session_averages = []
    for session_id in session_ids:
        session_mask = boulder_data['session_id'] == session_id
        session_data = boulder_data[session_mask]
        if not session_data.empty:
            session_climbs = [v_grade_to_numeric(grade) for climb_list in session_data['climbed'] for grade in climb_list]
            if session_climbs:
                avg = calculate_session_average(session_climbs)
                if avg is not None:
                    session_averages.append(avg)
    
    stats = {
        'Performance Metrics': {
            'Total Completed': len(completed_climbs),
            'Total Attempts': len(attempted_climbs),
            'Failure Rate': f"{failure_rate}%",
            'Average Grade': f"V{round(np.mean(completed_climbs), 1)}" if completed_climbs else "N/A",
            'Hardest Send': f"V{max(completed_climbs)}" if completed_climbs else "N/A",
            'Average of Top 20': f"V{round(np.mean(session_averages), 1)}" if session_averages else "N/A",
            'V6+ Percentage': f"{v6_plus_percentage}%"
        },
        'Session Data': {
            'Number of Sessions': len(session_ids),
            'Average Climbs/Session': round(len(completed_climbs) / len(session_ids), 1),
            'Total Duration': f"{selected_sessions['time'].sum()} min",
            'Average Duration': f"{round(selected_sessions['time'].mean(), 1)} min",
            'Total Calories': f"{selected_sessions['cal'].sum()} cal"
        }
    }
    
    return stats, completed_climbs, attempted_climbs