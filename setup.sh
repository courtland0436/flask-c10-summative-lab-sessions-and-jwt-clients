#!/bin/bash

# --- Setup Frontend ---
echo "Installing frontend dependencies..."
cd client-with-jwt
npm install
cd ..

# --- Setup Backend ---
echo "Installing backend dependencies and setting up database..."
cd server
pipenv install
pipenv run flask db upgrade
pipenv run python seed.py
cd ..

echo "--------------------------------------------"
echo "Setup complete!"
echo "To run the application:"
echo "1. In one terminal, navigate to /server and run 'pipenv run python app.py'"
echo "2. In another terminal, navigate to /client-with-jwt and run 'npm start'"
echo "--------------------------------------------"