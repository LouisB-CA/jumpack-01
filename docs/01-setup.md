# Best Practice
* Modern (2026) best practice is to always use a virtual environment.

# Initial Setup Considerations for RaspiOS 13
* There were changes to the OS that rendered the old venv stale.
<br>so this setup explicitly deletes the old venv

# Create a project directory
```bash
cd ~
PROJECT_DIR="$HOME/prgms/Python/jumpack-01"

# Create a project directory
mkdir -p "$PROJECT_DIR"
cd "$PROJECT_DIR"
```

## Remove and re-initialize the virtual environment
```bash
PROJECT_DIR="$HOME/prgms/Python/jumpack-01"
cd "$PROJECT_DIR"
rm -rf .venv

# Create a virtual environment
python3 -m venv .venv

# Activate it
source .venv/bin/activate

# Now install the libraries
pip install --upgrade pip
pip install --upgrade adafruit-circuitpython-ina228
pip install --upgrade matplotlib

# Print message
echo -e "\n\nDon't forget to use \`sudo ./.venv/bin/python ina228_test.py\` to execute!\n"

```

## Group *gpio* instead of *sudo*
* If the user is a member of group *gpio*, sudoer privileges are not required.
* First, see if the user is already a member
```bash
# Do this as a plain user
groups | tr ' ' '\' | grep gpio\|i2c\|spi
```
If the output is "gpio", "i2c" and "spi" you don't need sudoer privileges, you can use
```bash
python ina228_test.py
```
* To become a member, do this
```bash
sudo usermod -aG pi gpio,i2c,spi
```

## Activate I2C and SPI
* The INA228 communicates via I2C
* Neopixels require SPI.
* Do this as a plain user to check that these are active
```bash
raspi-config nonint get_i2c   # returns 0 = enabled, 1 = disabled
raspi-config nonint get_spi   # returns 0 = enabled, 1 = disabled
```


