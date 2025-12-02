#!/bin/bash

# Directory where your repo lives
REPO_DIR="/home/ubuntu/akash-url-shortner"

# Move into the repo directory
cd "$REPO_DIR" || { echo "Repo directory not found"; exit 1; }

# Fetch and pull latest changes
echo "Pulling latest changes..."
git pull origin develop   # change 'main' to 'master' or another branch if needed

echo "Done!"

# printing present working directory

pwd

#listing 

ls

#installing requirements and changing directory
cd app
source venv/bin/activate
echo "Installing dependencies..."
pip install -r requirements.txt 
echo "Done!"

#running uvicorn server 


# TIMESTAMP=$(date +"%Y-%m-%d_%H-%M-%S")
# LOGFILE="start_logs/uvicorn_$TIMESTAMP.log" #creating a logfile to save the start logs with timestamp

# mkdir -p start_logs

# nohup uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload > "$LOGFILE" 2>&1 & #2>&1 means: “send all error messages to the same place as standard output”
# echo "Uvicorn started in background. Logs: $LOGFILE"

TIMESTAMP=$(date +"%Y-%m-%d_%H-%M")

STARTUP_LOG="start_logs/uvicorn_start_$TIMESTAMP.log"
APP_LOG="api_logs/app_requests_$TIMESTAMP.log"

mkdir -p start_logs api_logs

# Run Uvicorn & pipe ONLY access logs to separate file
nohup uvicorn src.main:app \
    --host 0.0.0.0 --port 8000 --reload \
    --access-log \
    > "$STARTUP_LOG" 2>> "$APP_LOG" &