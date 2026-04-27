#!/usr/bin/env python3

"""
SIMULATE REAL TIME
Simulates power monitoring by writing dummy data to SQLite database
Based on INA228 Logger - Version 2
"""

import time
import board
import math
import sqlite3
import signal
import sys
import os
import argparse
from datetime import datetime
from pathlib import Path


# Configuration Constants
CONVERSION_TIME = 7      # 7 = 4120µs (maximum, best noise rejection)
AVERAGING_COUNT = 4      # 4 = 16 samples (2^4 = 16)
PID_FILE = "./ina228_simulator.pid"

# Global flag for clean shutdown
shutdown_requested = False

start_time = datetime.now()

def signal_handler(signum, frame):
    """Handle SIGTERM and SIGINT for clean shutdown"""
    global shutdown_requested
    shutdown_requested = True
    print("\nShutdown signal received, cleaning up...", file=sys.stderr)


def check_already_running():
    """Check if another instance is already running via PID file"""
    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, 'r') as f:
                old_pid = int(f.read().strip())
            
            # Check if process is still running
            try:
                os.kill(old_pid, 0)  # Doesn't actually kill, just checks if process exists
                print(f"Error: Logger already running with PID {old_pid}", file=sys.stderr)
                print(f"If this is incorrect, remove {PID_FILE} and try again", file=sys.stderr)
                return False
            except OSError:
                # Process doesn't exist, stale PID file
                print(f"Removing stale PID file (PID {old_pid} not running)", file=sys.stderr)
                os.remove(PID_FILE)
        except (ValueError, IOError) as e:
            print(f"Warning: Could not read PID file: {e}", file=sys.stderr)
            os.remove(PID_FILE)
    
    # Write current PID
    with open(PID_FILE, 'w') as f:
        f.write(str(os.getpid()))
    
    return True


def remove_pid_file():
    """Remove PID file on clean exit"""
    try:
        if os.path.exists(PID_FILE):
            os.remove(PID_FILE)
    except Exception as e:
        print(f"Warning: Could not remove PID file: {e}", file=sys.stderr)


def create_database(db_path):
    """Create database with readings and metadata tables"""
    conn = sqlite3.connect(db_path)
    
    # Main readings table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            current_a REAL,
            bus_voltage_v REAL,
            shunt_voltage_v REAL,
            power_w REAL,
            energy_j REAL,
            charge_c REAL,
            temperature_c REAL
        )
    """)
    
    # Metadata table
    conn.execute("""
        CREATE TABLE IF NOT EXISTS metadata (
            parameter_name TEXT PRIMARY KEY,
            parameter_value TEXT
        )
    """)
    
    conn.commit()
    return conn


def log_reading(conn, verbose=False):
    """Read from INA228 and log to database"""
    # Get current timestamp
    log_time = datetime.now()
    timestamp = log_time.isoformat().split('T')[1]  # skip the date, only the time of day
    omega = 0.05
    
    # Read all measurements (library returns SI base units)
    real_time = (log_time - start_time).total_seconds()
    current_a = .6+0.2*math.cos(omega*real_time)
    bus_voltage_v = 12 + 2*math.sin(omega*real_time)
    shunt_voltage_v = 0.03 * current_a
    power_w = current_a * bus_voltage_v
    energy_j = 0
    charge_c = 0
    temperature_c = 25
    
    # Insert into database
    conn.execute("""
        INSERT INTO readings 
        (timestamp, current_a, bus_voltage_v, shunt_voltage_v, 
         power_w, energy_j, charge_c, temperature_c)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (timestamp, current_a, bus_voltage_v, shunt_voltage_v,
          power_w, energy_j, charge_c, temperature_c))
    conn.commit()
    
    # Print to stdout if verbose (convert to human-friendly units)
    if verbose:
        time_str = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"{time_str} | {bus_voltage_v:7.3f}V | {current_a*1000:8.2f}mA")


def main():
    global shutdown_requested
    
    # Set up argument parser
    parser = argparse.ArgumentParser(description='INA228 Data Logger v2')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='Print readings to stdout')
    args = parser.parse_args()
    
    # Check if already running
    if not check_already_running():
        return 1
    
    # Register signal handlers
    signal.signal(signal.SIGTERM, signal_handler)
    signal.signal(signal.SIGINT, signal_handler)
    
    # Generate database filename with timestamp (no special chars)
    timestamp_str = datetime.now().strftime('%Y%m%d_%H%M%S')
    db_path = f"./Databases/jumpack_{timestamp_str}_simulated.db"
    
    # Print startup message
    print(f"Logger started, database: {db_path}")
    if args.verbose:
        print("Verbose mode enabled")
    
    # Create database
    try:
        conn = create_database(db_path)
    except Exception as e:
        print(f"Failed to create database: {e}", file=sys.stderr)
        remove_pid_file()
        return 1
    
    # Main logging loop
    try:
        while not shutdown_requested:
            time.sleep(2.0)
            log_reading(conn, verbose=args.verbose)
    except Exception as e:
        print(f"Error in logging loop: {e}", file=sys.stderr)
    finally:
        # Clean shutdown
        conn.close()
        remove_pid_file()
        print(f"Logger stopped, database closed: {db_path}")
    
    return 0


if __name__ == "__main__":
    sys.exit(main())


