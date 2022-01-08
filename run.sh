#Host the backend on port 5000
#!/bin/bash
pkill -f "python3.9" #janky way to stop old flask server
cd backend
python3.9 -m venv venv
source venv/bin/activate
/bin/bash -c 'source venv/bin/activate; gunicorn -w 24 --bind 0.0.0.0:5000 glint_server:app' &

# Host the frontend on port 3000
#export NODE_OPTIONS=--openssl-legacy-provider
cd ../frontend
npx -y serve dist