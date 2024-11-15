import json
import argparse
from datetime import datetime

def calculate_avg_value_per_climb(sessions, key):
    # For time, filter out invalid values (< 10 or > 300)
    if key == 'time':
        valid_sessions = [s for s in sessions if 10 <= s[key] <= 300]
    else:  # for calories
        valid_sessions = [s for s in sessions if s[key] > 0]
    
    if not valid_sessions:
        return None
    
    total_value = 0
    total_climbs = 0
    
    for session in valid_sessions:
        total_value += session[key]
        total_climbs += len(session['climbed'])
    
    return total_value / total_climbs

def interpolate_values(sessions):
    # Calculate averages
    avg_cal_per_climb = calculate_avg_value_per_climb(sessions, 'cal')
    avg_time_per_climb = calculate_avg_value_per_climb(sessions, 'time')
    
    new_sessions = []
    
    for session in sessions:
        new_session = session.copy()
        
        # Interpolate calories if needed
        if session['cal'] == 0 and avg_cal_per_climb is not None:
            num_climbs = len(session['climbed'])
            new_session['cal'] = round(avg_cal_per_climb * num_climbs)
        
        # Interpolate time if needed
        if (session['time'] < 10 or session['time'] > 300) and avg_time_per_climb is not None:
            num_climbs = len(session['climbed'])
            new_session['time'] = round(avg_time_per_climb * num_climbs)
        
        new_sessions.append(new_session)
    
    return new_sessions

def main():
    parser = argparse.ArgumentParser(description='Interpolate missing calories and invalid times in climbing data')
    parser.add_argument('input_file', help='Input JSON file path')
    parser.add_argument('output_file', help='Output JSON file path')
    
    args = parser.parse_args()
    
    try:
        # Read input file
        with open(args.input_file, 'r') as f:
            sessions = json.load(f)
        
        # Process the data
        new_sessions = interpolate_values(sessions)
        
        # Write output file
        with open(args.output_file, 'w') as f:
            json.dump(new_sessions, f, indent=2)
        
        # Print statistics
        avg_cal = calculate_avg_value_per_climb(sessions, 'cal')
        avg_time = calculate_avg_value_per_climb(sessions, 'time')
        
        print("\nInterpolation Statistics:")
        if avg_cal:
            print(f"Average calories per climb: {avg_cal:.2f}")
        else:
            print("No valid calorie data for interpolation")
            
        if avg_time:
            print(f"Average time per climb: {avg_time:.2f} minutes")
        else:
            print("No valid time data for interpolation")
            
        print(f"\nSuccessfully wrote interpolated data to {args.output_file}")
        
        # Print summary of changes
        changes = {
            'calories': sum(1 for s in sessions if s['cal'] == 0),
            'time': sum(1 for s in sessions if s['time'] < 10 or s['time'] > 300)
        }
        print("\nChanges made:")
        print(f"Interpolated calories for {changes['calories']} sessions")
        print(f"Interpolated time for {changes['time']} sessions")
    
    except FileNotFoundError:
        print(f"Error: Could not find input file {args.input_file}")
        exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON in input file {args.input_file}")
        exit(1)
    except PermissionError:
        print(f"Error: Permission denied when writing to {args.output_file}")
        exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()