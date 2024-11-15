#!/bin/bash

# Exit on any error
set -e

# Activate the virtual environment
if ! source /Users/clayarnold/Documents/Environments/Python/visualizations_environment/bin/activate; then
    echo "Failed to activate virtual environment"
    exit 1
fi

# Run the main processing script
if ! python3 main.py climbing_logs; then
    echo "Failed to process climbing logs"
    exit 1
fi

# Run the visualization script
if ! python3 climbing_graph_code.py; then
    echo "Failed to create visualizations"
    exit 1
fi

echo "Analysis completed successfully"
