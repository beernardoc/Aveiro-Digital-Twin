#!/bin/bash

# Clear the docker compose
cleanup() {
    echo "Stopping Frontend..."
    kill $FRONTEND_PID

    echo "Stopping Backend..."
    kill $BACKEND_PID

    echo "Stopping Docker Compose..."
    docker compose down

    exit 0
}

# Capture the signal to stop the script
trap cleanup INT

# Execute the docker compose with the database
docker compose up --build -d

# Execute the backend
cd backend
rm -rf venv
python3 -m venv venv
source venv/bin/activate
python3 -m pip install -r requirements.txt
python3 API/api.py &
BACKEND_PID=$!

# Execute the frontend
cd ../frontend/react-electron
npm install
npm run electron-react &
FRONTEND_PID=$!

# Mantain the script running, when the script is stopped, the docker compose is stopped
while :; do
    sleep 1
done
