
# Jumpack-01 battery charger monitor

The INA228 board is used to take 20-bit precision measuements during a battery charging session.
The board communicates with a headless RPi4 via I2C.  

Software is provided to store the data in an SQLite3 database, which can be accessed during the charging operation. 

Software is also provided that can be run from a remote location to plot the data as it is recorded.

The charger is a Coleman lantern wall wart rated at 13.5vdc and 400mA output.

The load is a Cobra Jumpack with input rated at 14vdc and 1A.

