# Timmy 
Timmy is a python cli for timesheeting that has the following
features:
- Parses Timesheet Entries in terminal using 
- Saves Timesheets to a text file
- Generates CSV's of timesheets

# Installation
Timmy uses python virtual environments. Eventually this will become a
single executable script that can be executed in bash
## Virtual Environment Setup
Setup and start the virtual environment in `./venv`
```bash
python3 venv venv
. ./venv/bin/activate
```
## Install Libraries
Ensure the virtual environment is running...
```bash
pip3 install -r requirements.txt
```
## Test the Script Modules
Ensure all modules pass their tests...
```bash
pytest
```
Alternatively, you can append `-s` to show logging outputs where they
are impelmented for further debugging...
## Run the Script
```bash
./main
```
