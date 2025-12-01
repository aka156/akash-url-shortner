#!/bin/bash

# Directory where your repo lives
REPO_DIR="/home/ubuntu/"

# Move into the repo directory
cd "$REPO_DIR" || { echo "Repo directory not found"; exit 1; }

# Fetch and pull latest changes
echo "Pulling latest changes..."
git pull origin develop   # change 'main' to 'master' or another branch if needed

echo "Done!"
