@echo off
title Car Information Database
 
echo Installing requirements...
python -m pip install -r requirements.txt --quiet
 
echo Starting the web GUI...
start "" http://localhost:5000
python carUserInterface.py