
# Jumpack-01 battery charger monitor
**Runs on:** [ RPi4, x86 ]

**Languages:** Python, SQL, bash

**Status:** Active

## Hardware Dependencies

| Main Component | Host | Role |
|-----------|------|------|
| ina228_logger_*.py | RPi4 | polls the sensor, writes SQLite DB |
| monitor-xx.py | x86 | Reads DB, renders real-time plot |


| Support | Host | Role |
|-----------|------|------|
| simulate_real_time.py | RPi4 | playback |
| dump.py, generate_test_data.py | debugging |

## Description

The INA228 board is used to take 20-bit precision measuements during a battery charging session.
The board communicates with a headless RPi4 via I2C.  

Software is provided to store the data in an SQLite3 database, which can be accessed during the charging operation. 

Software is also provided that can be run from a remote location to plot the data as it is recorded.

The charger is a Coleman lantern wall wart rated at 13.5vdc and 400mA output.

The load is a Cobra Jumpack with input rated at 14vdc and 1A.


