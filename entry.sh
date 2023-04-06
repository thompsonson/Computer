#!/bin/bash
python interfaces/bot_telegram.py &
cd interfaces
export FLASK_APP=www
export FLASK_ENV=development
flask run --host 0.0.0.0 --port 8080

