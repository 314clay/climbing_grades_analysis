# Climbing Log Parser

This Python script processes climbing log files and generates a JSON output with parsed data.

## Features

- Processes multiple climbing log files from a specified folder
- Extracts information such as date, climb type, grades attempted, grades climbed, time, and calories
- Outputs results to a single JSON file

## Requirements

- Python 3.6 or higher

## Usage

1. Clone or download this repository to your local machine.

2. Open a terminal and navigate to the directory containing the script.

3. Run the script using the following command:

   ```
   python climbing_log_parser.py path/to/your/folder -o output_file.json
   ```

   Replace `path/to/your/folder` with the actual path to the folder containing your climbing log files.

   The `-o` argument is optional. If you don't specify it, the script will save the results to `climbing_results.json` in the current directory.

## Example

```
python climbing_log_parser.py ./climbing_logs -o my_climbing_data.json
```

This command will process all .txt files in the `./climbing_logs` folder and save the results to `my_climbing_data.json`.

## Input File Format

The script expects each climbing log file to have the following format:

```
[Date] at [Time]
[Climb Type]
[Grade]: [Emoji indicators]
...
Max: [Max grade]
Pinnacle Climb Log -
Time
[Duration]
Cal
[Calories]
```

## Output

The script generates a JSON file containing an array of objects, each representing a parsed climbing log. Each object includes:

- `type`: The type of climb
- `date`: The date and time of the climb in ISO format
- `time`: The duration of the climb in minutes
- `cal`: The number of calories burned
- `attempted`: An array of grade labels for all attempts (including both successful and unsuccessful)
- `climbed`: An array of grade labels for successfully climbed routes

Example output structure:

```json
{
  "type": "Boulder",
  "date": "2024-10-11T01:08:00",
  "time": 118,
  "cal": 966,
  "attempted": ["V2", "V3", "V3", "V3", "V4", "V4", "V4", "V4", "V5", "V5", "V6", "V7"],
  "climbed": ["V2", "V3", "V3", "V3", "V4", "V4", "V4", "V4", "V5", "V5", "V6", "V7"]
}
```

## Troubleshooting

If you encounter any issues, make sure:
- The input folder path is correct
- You have read permissions for the input folder and files
- You have write permissions for the output file location

For any other problems, please open an issue in the repository.