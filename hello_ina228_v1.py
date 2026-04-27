#!/usr/bin/env python3

"""
Hello INA228 - Basic Power Monitoring Script
Reads voltage, current, power, and temperature from INA228
"""

import time
import board
import adafruit_ina228

def main():
    print("=" * 60)
    print("Hello INA228 - Power Monitor Test")
    print("=" * 60)

    # Initialize I2C bus
    try:
        i2c = board.I2C()
        print("✓ I2C bus initialized")
    except Exception as e:
        print(f"✗ Failed to initialize I2C: {e}")
        return

    # Initialize INA228 sensor
    try:
        ina228 = adafruit_ina228.INA228(i2c)
        print("✓ INA228 detected at address 0x40")
        ina228._alert_conv = False
    except Exception as e:
        print(f"✗ Failed to detect INA228: {e}")
        print("  Check wiring and run 'sudo i2cdetect -y 1'")
        return

    # Configure the sensor
    # Shunt resistor: 15 milliohms (0.015 ohms)
    # Max expected current: 600mA (0.6A)
    print("\nConfiguration:")
    print(f"  Shunt resistor: 15 mΩ (0.015 Ω)")
    print(f"  Max current: 600 mA")
    print(f"  Bus conversion time: {ina228.bus_voltage_conv_time} µs")
    print(f"  Shunt conversion time: {ina228.shunt_voltage_conv_time} µs")
    print(f"  Averaging count: {ina228.averaging_count}")
    
    print("\n" + "=" * 60)
    print("Starting continuous measurements (Ctrl+C to stop)")
    print("=" * 60)
    print()
    
    # Continuous measurement loop
    try:
        while True:
            # Wait 2 seconds before next reading
            time.sleep(2)

            # Read all measurements
            current_ma = ina228.current * 1000
            bus_voltage = ina228.bus_voltage
            shunt_voltage_mv = ina228.shunt_voltage * 1000  # Convert V to mV
            power_mw = ina228.power * 1000
            energy_j = ina228.energy
            temp_c = ina228.die_temperature
            
            # Display results
            print(f"Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
            print(f"  Current:       {current_ma:8.2f} mA")
            print(f"  Bus Voltage:   {bus_voltage:8.3f} V")
            print(f"  Shunt Voltage: {shunt_voltage_mv:8.3f} mV")
            print(f"  Power:         {power_mw:8.2f} mW")
            print(f"  Energy:        {energy_j:8.2f} J")
            print(f"  Temperature:   {temp_c:8.2f} °C")
            print("-" * 60)

    except KeyboardInterrupt:
        print("\n\nMeasurement stopped by user")
        # Optional: Put INA228 into shutdown mode to save power
        ina228.mode = adafruit_ina228.Mode.SHUTDOWN
        print("=" * 60)

if __name__ == "__main__":
    main()


