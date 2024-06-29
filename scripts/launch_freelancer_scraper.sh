#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
parent="$(dirname "$DIR")"

# Activate virtualenv
source /path/to/your/venv/activate

# Run
nohup /path/to/your/venv/bin/python "$parent/freelancer_scraper.py" > /dev/null 2>&1 &
