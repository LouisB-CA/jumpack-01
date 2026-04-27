
# Workflow
* Activate the virtual environment
* Start the logger program, which must run with root permissions
  <br> `sudo ./.venv/bin/python ./ina228_logger_v2.py &`

* Plug in the Jumpack and the Coleman wall wart

## Options for monitoring the readings
* Include the --verbose flag as an argument to the ina228_logger_v2 python
* Monitor the charging current and voltage with SQL queries
* Use ***waypipe*** to view the plots on a desktop computer
  <br> `waypipe ssh pi@cygnus "cd ~/prgms/Python/jumpack-01 && python monitor-02.py"`

