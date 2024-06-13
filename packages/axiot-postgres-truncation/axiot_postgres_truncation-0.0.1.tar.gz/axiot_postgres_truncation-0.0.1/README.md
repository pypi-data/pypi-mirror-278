# Introduction 
TODO: Truncating the Data stored in Postgres DB and moving into history for Performance Improvement 

# Migration
This python repository helps to Truncating the Data stored in Postgres DB and moving into history for Performance Improvement .

## Running locally
- run setup .py
- Run script `python filename enviornment projectname` or `python3 filename enviornment projectname `
- filename
  - main.py starting file of the program
- environment 
  - dev  (Development server for Dev team)
  - qa   (QA server once Dev team unit tested and released to QA team)
  - prod (Prod server once QA team unit tested and released to Production for Client)
- projectname
  - alteem
  - jjm
  - arion etc...
- Sample Run script `python main.py dev alteem` or `python3 main.py dev alteem `
- To Help `python migrate.py -h`