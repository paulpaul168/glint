#!/bin/bash
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
FLASK_APP=glint_server FLASK_ENV=development flask run
