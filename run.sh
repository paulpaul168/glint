#Host the backend on port 500
#!/bin/bash
pkill -f "python3.9" #janky way to stop old flask server
cd backend
python3.9 -m venv venv
source venv/bin/activate
FLASK_APP=glint_server FLASK_ENV=development flask run &

# Host the frontend on port 3000
#export NODE_OPTIONS=--openssl-legacy-provider
cd ../frontend
npx -y serve dist