# Battery Charging Monitor System - Specification
Version 1.0 -- 2026-01-15

## Context and Purpose

I have a Cobra Model CPP 7500 JumPack battery that I charge using a Coleman 13.5V/600mA wall wart. The charging process takes several hours (maybe up to 10 hours), and I want to collect detailed data about voltage and current throughout the charge cycle so I can analyze it later. I also want to watch the charging process in real-time from my terminal over SSH.

I have developed this specification to help you, Claude, understand the big picture as well as some dtails.  I want to conduct a series of chats to develop a series of programs.  Each program builds on or is nependent on the next.  

If you have any questions, ask for clarification.  

## Hardware Configuration

* Raspberry Pi 4 running raspios 11 bullseye with Python 3.9.2
* Adafruit INA228 breakout board connected via I2C
  - I2C pins are GPIO2 and GPIO3, physical pins 3 and 5
  - address 0x40
  - I have verified the address with CLI commands `i2cdetect -y 1` and `i2cdump -y 1 0x40`
* The INA228 has a R015 (15 mohms) shunt resistor soldered on the breakout board
* The INA228 is wired for high-side measurement, meaning it sits between the charger and the battery positive terminal

* There is one Neopixel LED at GPIO18 (physical pin 12)
  - Don't be concerned if the programs don't use this.  
  - Intended only for that later enhancement, but available.  

## What I Want to Build

This should be three separate Python programs that work together:

### Program 1: Sensor Test (ina228_test.py)

This is just a sanity check before I commit to a long data collection run. When I run it, it should:
- Try to find the INA228 on the I2C bus
- If found, read one sample of raw data from all registers
- Print the raw register values to the terminal with labels
- Convert and display: bus voltage (V), shunt voltage (mV), and current (mA)
- Tell me if it can't find the sensor or if I2C communication fails
- Then exit

This program should be simple enough that if it works, I know the hardware is connected correctly.

### Program 2: Background Data Logger (charge_logger.py)

This is the program that runs for hours collecting data in the background. When I start it, it should:
* Open the INA228 and verify it's responding
* Create a new JSON log file with a timestamp in the filename, like: `charge_log_2026-01-15_14-30-00.json`
* Save this file in directory ./Data/
* Every 2 seconds (adjustable), read voltage and current from the INA228
* Append a JSON object to the log file with: ISO timestamp, human readable time, raw register values, and calculated voltage/current
* If there's an I2C error, log it but keep trying
* Run until I kill it with Ctrl-C or SIGINT, then close the file cleanly
* Print minimal output - just a startup message and maybe a dot every 100 samples so I know it's alive
  - Program will run in the background using nohup with output redirected to a log file

The JSON structure should be an array of measurement objects. Each object needs enough information that I can recalculate anything later if I discover my conversion math was wrong.  The data will be used to predict the time to full charge.  

### Program 3: Real-Time Monitor (charge_monitor.py)

This program watches the log file and shows me what's happening. When I run it:
* Ask me which log file to monitor (or auto-detect the most recent one in the logging directory)
* Open that file and seek to the end
* Every 5 seconds, read any new entries and display the latest values in a clear format:
  - Current time
  - Bus voltage (V, 2 decimal places)
  - Current (mA, 1 decimal place)
  - Power (W, 2 decimal places)
  - Total charge delivered so far (amp-hours, 3 decimal places)
* Handle the case where the logger hasn't written new data yet
* Exit cleanly on Ctrl-C

### Future Enhancement - NeoPixel Manager (optional, not priority)

Eventually I might write a fourth program that manages NeoPixels as a daemon, accepting simple commands like "2 255 0 0" to set pixel 2 to red. But let's save this for dessert - not the immediate priority.

I already have a working python blinky script that flashes various colors on the neopixel. If you want to add neopixel support to any program, be sure to ask me for the blinky script, so you can see what works.  But I think we should not need neopixel support to the first 3 programs.

## Technical Constraints

* I'll be running everything over SSH, so no GUI
* I need to be able to start the logger, disconnect my SSH session, and have it keep running
* The monitor program should work even if I start it hours after the logger started, or if the logger is not running.
* Use a Python virtual environment with dependencies listed in requirements.txt
* Error messages should be clear enough that I can tell what went wrong without reading code

## Development Workflow

We'll build these programs iteratively:
1. Start with Program 1 (sensor test) to verify hardware
2. Once that works, build Program 2 (data logger)
3. Then Program 3 (monitor)
4. NeoPixel manager comes later

When debugging, we'll use version labels like "Version 1", "Version 2", etc. so we know exactly which version we're discussing.  Whenever you give me a first version or a new version, always give it a new identifier (version number) so we can stay on the same page.

We will start a new chat for each of these programs.  Notes and source code from previous chats may be available or can be made available.  



