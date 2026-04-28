
# How to Monitor the Charging Process

## Rough - needs checking

1. activate the virtual environment - do this as user pi on RPi
2. start the logger in the background - root privileges may be required
3. connect the Coleman power supply and the Jumpack battery
4. create a symlink, charging.db, to the running sqlite3 database
5. on the debian desktop, run 
	`ssh -Y cygnus 'cd ~/prgms/Python/jumpack-01/ && ./.venv/bin/python monitor-02.py'

6. on the RPi, monitor the progress with the *sql_queries.sh* script

## How monitor-02.py works


