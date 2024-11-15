import json
from datetime import datetime
import re
import os
import argparse

def parse_climbing_log(file_path):
    with open(file_path, 'r') as file:
        lines = [line.strip() for line in file if line.strip()]
    
    date_str = lines[0]
    date = datetime.strptime(date_str, "%B %d, %Y at %I:%M %p")
    
    climb_type = lines[1]
    
    attempted = []
    climbed = []
    
    for line in lines[2:]:
        if line.startswith("Max:") or line.startswith("Pinnacle Climb Log"):
            break
        if ':' in line:
            grade, emojis = line.split(':')
            grade = grade.strip()
            green_count = emojis.count('🟢')
            yellow_count = emojis.count('🟡')
            
            climbed.extend([grade] * green_count)
            attempted.extend([grade] * yellow_count)
    
    content = ' '.join(lines)
    
    time_match = re.search(r'(\d+)h (\d+)m', content)
    total_minutes = 0
    if time_match:
        hours, minutes = map(int, time_match.groups())
        total_minutes = hours * 60 + minutes
    
    cal_match = re.search(r'([\d,]+) Cal', content)
    calories = 0
    if cal_match:
        calories = int(cal_match.group(1).replace(',', ''))
    
    return {
        "type": climb_type,
        "date": date.isoformat(),
        "time": total_minutes,
        "cal": calories,
        "attempted": attempted,
        "climbed": climbed
    }

def process_folder(folder_path, output_file):
    results = []
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            result = parse_climbing_log(file_path)
            results.append(result)
        except Exception as e:
            print(f"Error processing {filename}: {e}")
    
    results.sort(key=lambda x: x['date'])  # Sort results by date
    
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"Processed {len(results)} files. Results saved to {output_file}")

def main():
    parser = argparse.ArgumentParser(description="Process climbing log files from a folder.")
    parser.add_argument("folder", help="Path to the folder containing climbing log files")
    parser.add_argument("-o", "--output", default="climbing_results.json", help="Output file name (default: climbing_results.json)")
    
    args = parser.parse_args()
    
    process_folder(args.folder, args.output)

if __name__ == "__main__":
    main()