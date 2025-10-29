#!/bin/bash

# Configuration - modify these as needed
DATAPATH="${DATAPATH:-/alf/data/emcal/OfflineTrigger/filelistsQA/results}"
PORT="${PORT:-13356}"

# Setup
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment and install requirements
source venv/bin/activate
pip install -q -r requirements.txt

# Export DATAPATH and run the application
export DATAPATH
echo "Starting webapp on port $PORT with DATAPATH=$DATAPATH"
echo "Access at: http://localhost:$PORT"

flask --app wsgi:application run --host=0.0.0.0 --port=$PORT --debug
