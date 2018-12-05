# Logs Analysis Project

> Created By Abdirashiid Jama

## About

You will use this 'internal reporting tool' that will comb through a large database and return the information you require

## To Run

### You will need:
- Python3
- Vagrant
- VirtualBox

### Getting Ready
1. Install Vagrant And VirtualBox
2. Clone this repository

### Running the program

Launch Vagrant VM by running `vagrant up`, you can the log in with `vagrant ssh`

To load the data, use the command `psql -d news -f newsdata.sql` to connect a database and run the necessary SQL statements.

The database includes three tables:
- Authors table
- Articles table
- Log table

To execute the program, run `python3 report-tool.py` from the command line.