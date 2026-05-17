#!/usr/bin/env python3

"""
INA228 Logger - Version 1
Logs INA228 power monitoring data to SQLite database
"""

import board
import adafruit_ina228
import sqlite3
import signal
import functools, sys, time
import argparse
from datetime import datetime
from pathlib import Path


# Global flag for clean shutdown
shutdown_requested = False


def signal_handler(signum, frame):
    """Handle SIGTERM and SIGINT for clean shutdown"""
    global shutdown_requested
    shutdown_requested = True
    print("\nShutdown signal received, cleaning up...", file=sys.stderr)


def create_database(db_path):
    """Create database and readings table"""
    conn = sqlite3.connect(db_path)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            current_a REAL,
            bus_voltage_v REAL,
            shunt_voltage_v REAL,
            power_w REAL,
            energy_j REAL,
            temperature_c REAL
        )
    """)
    conn.commit()
    return conn


def log_reading(conn, ina228, verbose=False):
    """Read from INA228 and log to database"""
    # Get current timestamp
    timestamp = datetime.now().isoformat()
    
    # Read all measurements (SI units throughout)
    current_a = ina228.current
    bus_voltage_v = ina228.bus_voltage
    shunt_voltage_v = ina228.shunt_voltage
    power_w = ina228.power
    energy_j = ina228.energy
    temperature_c = ina228.die_temperature
    
    # Insert into database
    conn.execute("""
        INSERT INTO readings 
        (timestamp, current_a, bus_voltage_v, shunt_voltage_v, 
         power_w, energy_j, temperature_c)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (timestamp, current_a, bus_voltage_v, shunt_voltage_v,
          power_w, energy_j, temperature_c))
    conn.commit()
    
    # Print to stdout if verbose
    if verbose:
        time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"{time_str} | {bus_voltage_v:7.3f}V | {current_a*1000:8.2f}mA")


def main():
    global shutdown_requested
    
    # Set up argument parser
    parser = argparse.ArgumentParser(description='INA228 Data Logger')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Print readings to stdout')
    args = parser.parse_args()
    
    # Register signal handlers
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Generate database filename with timestamp
    timestamp_str = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    db_path = f"./databases/jumpack_{timestamp_str}.db"
    
    # Print startup message
    print(f"Logger started, database: {db_path}")
    if args.verbose:
        print("Verbose mode enabled")
    
    # Initialize I2C and INA228
    try:
        i2c = board.I2C()
        ina228 = adafruit_ina228.INA228(i2c)
        ina228._alert_conv = False
    except Exception as e:
        print(f"Failed to initialize INA228: {e}", file=sys.stderr)
        return 1
    
    # Create database
    try:
        conn = create_database(db_path)
    except Exception as e:
        print(f"Failed to create database: {e}", file=sys.stderr)
        return 1
    
    # Main logging loop
    try:
        while not shutdown_requested:
            log_reading(conn, ina228, verbose=args.verbose)
            time.sleep(0.20)
    except Exception as e:
        print(f"Error in logging loop: {e}", file=sys.stderr)
    finally:
        # Clean shutdown
        conn.close()
        print(f"Logger stopped, database closed: {db_path}")
    
    return 0


if __name__ == "__main__":
    print = functools.partial(print, flush=True)
    sys.exit(main())

