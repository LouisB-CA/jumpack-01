Using CircuitPython on a Raspberry Pi 4 requires the [Adafruit Blinka](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/overview) library, which translates CircuitPython APIs to work on Linux. [1] 
## 1. Pre-requisites
Before running code, you must enable I2C on your Raspberry Pi: [2] 

* Enable I2C: Use the terminal command sudo raspi-config and navigate to Interfacing Options > I2C to enable the bus.
* Install Blinka: Run pip3 install adafruit-blinka to provide the board and busio modules. [1, 3, 4, 5, 6] 

## 2. Basic I2C Scan Example
This "Hello World" of I2C identifies the hexadecimal addresses of all connected devices on the default bus. [7, 8] 

import timeimport board
# Initialize the I2C bus using the board's default SCL and SDA pinsi2c = board.I2C()
while not i2c.try_lock():
    pass
try:
    while True:
        # Scan for devices and print their addresses in hex format
        addresses = [hex(device_address) for device_address in i2c.scan()]
        print("I2C addresses found:", addresses)
        time.sleep(2)finally:
    # Always unlock the bus for other processes when finished
    i2c.unlock()

[9, 10] 
## 3. Reading and Writing to a Device
For more direct interaction with a specific sensor (e.g., at address 0x18), you can use the writeto and readfrom_into methods. [11] 

import boardimport busio
# Create I2C busi2c = busio.I2C(board.SCL, board.SDA)
# Lock the bus before starting a transactionwhile not i2c.try_lock():
    pass
try:
    # Example: Write one byte (0x05) to request data from a specific register
    # Device address is 0x18
    i2c.writeto(0x18, bytes([0x05]))

    # Prepare a buffer to hold the 2 bytes of incoming data
    result = bytearray(2)
    i2c.readfrom_into(0x18, result)
    
    print("Received data:", [hex(b) for b in result])finally:
    i2c.unlock()

[11, 12, 13] 
## Wiring Guide

| Raspberry Pi 4 Pin [14, 15, 16, 17, 18] | I2C Device Pin |
|---|---|
| 3.3V (Pin 1) | VIN / VCC |
| GND (Pin 6/9) | GND |
| SDA (Pin 3 / GPIO 2) | SDA |
| SCL (Pin 5 / GPIO 3) | SCL |

[18, 19, 20] 
Do you need an example for a specific sensor or help troubleshooting a connection error?

[1] [https://learn.adafruit.com](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/overview)
[2] [https://www.abelectronics.co.uk](https://www.abelectronics.co.uk/kb/article/1/i2c-part-2-enabling-i2c-on-the-raspberry-pi#:~:text=Enabling%20I%C2%B2C%20in%20the%20Linux%20Terminal%0A%0AStep%201:,3%20Interface%20Options%20and%20then%20I5%20I2C.)
[3] [https://learn.sparkfun.com](https://learn.sparkfun.com/tutorials/raspberry-pi-spi-and-i2c-tutorial/i2c-on-pi)
[4] [https://openest.io](https://openest.io/non-classe-en/activate-raspberry-pi-4-i2c-bus/#:~:text=Configuring%20the%20firmware%20of%20the%20Raspberry%2DPi%204,enable%20the%20i2c%2D1%20bus%20via%20the%20config.)
[5] [https://learn.adafruit.com](https://learn.adafruit.com/adafruit-ltc4316-i2c-address-translator/circuitpython-and-python)
[6] [https://learn.adafruit.com](https://learn.adafruit.com/adafruit-neodriver-i2c-to-neopixel-driver/circuitpython-and-python#:~:text=The%20go%2Dto%20way%20to%20instantiate%20I2C%20in,to%20switch%20to%20the%20Adafruit_Extended_Bus%20helper%20library.)
[7] [https://www.youtube.com](https://www.youtube.com/watch?v=0cnNj4qwTAk)
[8] [https://learn.adafruit.com](https://learn.adafruit.com/scanning-i2c-addresses/raspberry-pi)
[9] [https://learn.adafruit.com](https://learn.adafruit.com/scanning-i2c-addresses/circuitpython)
[10] [https://raspberrypi.stackexchange.com](https://raspberrypi.stackexchange.com/questions/132559/circuitpython-interface-with-i2c-device#:~:text=Adafruit%20has%20the%20following%20code:%20%22%22%22CircuitPython%20Essentials,when%20ctrl%2Dc%27ing%20out%20of%20the%20loop%20i2c.unlock%28%29)
[11] [https://www.digikey.com](https://www.digikey.com/en/maker/projects/circuitpython-basics-i2c-and-spi/9799e0554de14af3850975dfb0174ae3)
[12] [https://docs.circuitpython.org](https://docs.circuitpython.org/en/10.1.0/shared-bindings/i2ctarget/index.html)
[13] [https://emalliab.wordpress.com](https://emalliab.wordpress.com/2022/01/04/reading-i2c-registers-from-circuitpython/#:~:text=i2cbus%20=%20board.I2C%28%29%20def%20i2c_read_reg%28i2cbus%2C%20addr%2C%20reg%2C,=%20reg%20buf.extend%28data%29%20i2cbus.writeto%28addr%2C%20buf%29%20finally:%20i2cbus.unlock%28%29)
[14] [https://learn.adafruit.com](https://learn.adafruit.com/adafruit-neodriver-i2c-to-neopixel-driver/circuitpython-and-python#:~:text=Here%27s%20the%20Raspberry%20Pi%20wired%20with%20I2C,NeoPixel%20ground%20to%20driver%20G%20%28black%20wire%29)
[15] [https://www.instructables.com](https://www.instructables.com/Measuring-Temperature-With-I2C-Sensor-LM75A-on-Ras/)
[16] [https://www.halvorsen.blog](https://www.halvorsen.blog/documents/programming/python/resources/powerpoints/Raspberry%20Pi%20and%20CircuitPython.pdf)
[17] [https://roboticsbackend.com](https://roboticsbackend.com/wiringpi-i2c-tutorial-rasperry-pi-adxl345/)
[18] [https://learn.adafruit.com](https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/i2c-sensors-and-devices)
[19] [https://learn.adafruit.com](https://learn.adafruit.com/adafruit-pcf8575/python-circuitpython)
[20] [https://pinout.xyz](https://pinout.xyz/pinout/i2c#:~:text=I2C%20%2D%20Inter%20Integrated%20Circuit%20GPIO%202,fixed%201.8%20k%CE%A9%20pull%2Dup%20resistor%20to%203.3v.)

