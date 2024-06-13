@echo off
cd C:\Users\sampy\Downloads\Campain\local\1
myenv\Scripts\activate
python app.py > output.log 2>&1
deactivate