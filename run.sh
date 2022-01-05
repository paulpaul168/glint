#!/bin/bash
cd backend
python3.9 -m venv venv
source venv/bin/activate
FLASK_APP=glint_server FLASK_ENV=development flask run &

export NODE_OPTIONS=--openssl-legacy-provider
cd ../frontend
serve -s dist