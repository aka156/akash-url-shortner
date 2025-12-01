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