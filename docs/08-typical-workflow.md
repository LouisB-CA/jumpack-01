
# Jumpack-01 battery charger monitor

## In a nutshell
1. Check the wiring
2. Activate the venv
3. Run the ina228 monitor in the background
4. Plug in the charger and the battery
5. Run the monitor program via ssh to plot the data
6. Wait till the current drops to zero

## Typical Workflow
* Do this on the headless RPi4
```bash
PROJECT_DIR="$HOME/prgms/Python/jumpack-01"
cd "$PROJECT_DIR"

source .venv/bin/activate

# Note the use of (1) sudo and (2) the local python
sudo ./.venv/bin/python ina228_logger_v2.py &
```
* Do this on the desktop computer
```bash
ssh -Y cygnus 'cd ~/prgms/Python/jumpack-01/ && python monitor-02.py
```

