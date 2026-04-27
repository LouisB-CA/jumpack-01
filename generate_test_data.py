#!/usr/bin/env python

#
# Generate test data for RDB table
# this data is used to test the plot routines
#

import sqlite3
import math
from datetime import datetime, timedelta

DB_PATH = "./Databases/jumpack_3000_dummy.db"  # change this to your actual database path

# Parameters
N = 1000
dt = 0.25          # seconds per step
w = 1 / 12.0       # angular frequency (rad/s) — ~2-3 full sine waves over 1000 steps

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


# Numerical integration accumulators
charge = 0.0
energy = 0.0

rows = []
start_time = datetime.now()

for i in range(N):
    t = i * dt
    timestamp = (start_time + timedelta(seconds=t)).isoformat(timespec='milliseconds')

    voltage   = 12.0 + 2.0 * math.sin(w * t)
    current   = 0.6  + 0.2 * math.cos(w * t)
    power     = voltage * current

    # Integrate using rectangle rule
    charge += current * dt
    energy += power   * dt

    rows.append((
        timestamp,
        current,       # current_a
        voltage,       # bus_voltage_v
        0.0,           # shunt_voltage_v
        power,         # power_w
        energy,        # energy_j
        charge,        # charge_c
        0.0,           # temperature_c
    ))

## conn = sqlite3.connect(DB_PATH)
conn = create_database(DB_PATH)
cur  = conn.cursor()

cur.executemany("""
    INSERT INTO readings
        (timestamp, current_a, bus_voltage_v, shunt_voltage_v,
         power_w, energy_j, charge_c, temperature_c)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", rows)

# Optionally record metadata about this test run
cur.execute("""
    INSERT OR REPLACE INTO metadata (parameter_name, parameter_value)
    VALUES ('test_data_generated', ?)
""", (datetime.now().isoformat(),))

conn.commit()
conn.close()

print(f"Inserted {N} rows into '{DB_PATH}'.")
print(f"Time span : {N * dt:.1f} s  ({N * dt / 60:.2f} min)")
print(f"w         : {w:.4f} rad/s  →  period ≈ {2*math.pi/w:.1f} s")
print(f"# cycles  : {N * dt * w / (2 * math.pi):.2f}")
print(f"Final charge : {charge:.3f} C")
print(f"Final energy : {energy:.3f} J")

