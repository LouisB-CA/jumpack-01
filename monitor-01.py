#!/usr/bin/env python3
"""
Simple JumPack Monitor - Plots voltage and current from SQLite database
Usage: python jumpack_monitor.py [--auto-refresh]
"""

import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime
import subprocess
import sys
import time
import argparse

# Configuration
RPI_HOST = "pi@192.168.12.213"
RPI_DB_PATH = "/home/pi/prgms/Python/jumpack-01/Databases/jumpack_2026-01-17_20-28-51.db"
LOCAL_DB_PATH = "/tmp/jumpack_monitor.db"

def fetch_database():
    """Copy database from RPi using scp"""
    cmd = ["scp", f"{RPI_HOST}:{RPI_DB_PATH}", LOCAL_DB_PATH]
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error fetching database: {e}", file=sys.stderr)
        return False

def read_data():
    """Read voltage and current data from database"""
    conn = sqlite3.connect(LOCAL_DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT timestamp, bus_voltage_v, current_a 
        FROM readings 
        ORDER BY id
    """)
    
    data = cursor.fetchall()
    conn.close()
    
    if not data:
        return None, None, None
    
    # Parse timestamps and convert to minutes from start
    timestamps = [datetime.fromisoformat(row[0]) for row in data]
    start_time = timestamps[0]
    times_min = [(t - start_time).total_seconds() / 60 for t in timestamps]
    
    voltages = [row[1] for row in data]
    currents = [row[2] * 1000 for row in data]  # Convert to mA
    
    return times_min, voltages, currents

def plot_data(times_min, voltages, currents):
    """Create plots of voltage and current vs time"""
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
    
    # Voltage plot
    ax1.plot(times_min, voltages, 'b-', linewidth=1)
    ax1.set_ylabel('Bus Voltage (V)', fontsize=12)
    ax1.set_title('JumPack Charging Monitor', fontsize=14, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Current plot
    ax2.plot(times_min, currents, 'r-', linewidth=1)
    ax2.set_xlabel('Time (minutes)', fontsize=12)
    ax2.set_ylabel('Current (mA)', fontsize=12)
    ax2.grid(True, alpha=0.3)
    
    # Add statistics
    avg_voltage = sum(voltages) / len(voltages)
    avg_current = sum(currents) / len(currents)
    duration = times_min[-1] if times_min else 0
    
    stats_text = f'Duration: {duration:.1f} min | Avg V: {avg_voltage:.2f}V | Avg I: {avg_current:.1f}mA'
    fig.text(0.5, 0.02, stats_text, ha='center', fontsize=10, style='italic')
    
    plt.tight_layout(rect=[0, 0.03, 1, 1])
    return fig

def main():
    parser = argparse.ArgumentParser(description='JumPack Monitor')
    parser.add_argument('--auto-refresh', action='store_true',
                       help='Auto-refresh plot every 30 seconds')
    parser.add_argument('--interval', type=int, default=30,
                       help='Refresh interval in seconds (default: 30)')
    args = parser.parse_args()
    
    plt.ion() if args.auto_refresh else plt.ioff()
    
    while True:
        print("Fetching database from RPi...", end=' ')
        if not fetch_database():
            print("FAILED")
            if not args.auto_refresh:
                return 1
            time.sleep(args.interval)
            continue
        print("OK")
        
        print("Reading data...", end=' ')
        times_min, voltages, currents = read_data()
        if times_min is None:
            print("No data found")
            if not args.auto_refresh:
                return 1
            time.sleep(args.interval)
            continue
        print(f"{len(times_min)} readings")
        
        print("Generating plots...")
        plt.close('all')
        fig = plot_data(times_min, voltages, currents)
        
        if args.auto_refresh:
            plt.draw()
            plt.pause(0.1)
            print(f"Waiting {args.interval} seconds until next refresh...\n")
            time.sleep(args.interval)
        else:
            plt.show()
            break
    
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nMonitoring stopped by user")
        sys.exit(0)


