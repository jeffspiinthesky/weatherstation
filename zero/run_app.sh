#!/bin/bash

cd /home/pi/src/weatherstation/zero
export FLASK_APP=app
flask run --host=0.0.0.0 &
firefox -kiosk -private-window http://localhost:5000


