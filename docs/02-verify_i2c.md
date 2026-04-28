# I2C Command Reference for INA228
* This doc assumes the I2C address of the INA228 is 0x40

## Verify I2C is enabled
```bash
raspi-config nonint get_i2c   # returns 0 = enabled, 1 = disabled
```

## Using i2cdetect to Find Device Address
```bash
i2cdetect -y 1
```

This scans I2C bus 1 and shows a grid of addresses. Your INA228 will show up as a two-digit hex number (like `40`, `45`, etc.) in the grid. Everything else will show `--`.

The `-y` flag means "yes, just do it" (skips the warning prompt).

## What You'll See
```
     0  1  2  3  4  5  6  7  8  9  a  b  c  d  e  f
00:          -- -- -- -- -- -- -- -- -- -- -- -- -- 
10: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
20: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
30: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
40: 45 -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
50: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
60: -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- 
70: -- -- -- -- -- -- -- --
```

In this example, the device is at address `0x45`.

## Other Useful I2C Commands

### List Available I2C Buses
```bash
i2cdetect -l
```

### Read Single Byte from Register
```bash
# Read from register 0x00 on device at 0x45
i2cget -y 1 0x40 0x00
```

### Dump All Registers
```bash
# Shows first 256 bytes of register space
i2cdump -y 1 0x40
```

### Write to Register (Use Carefully)
```bash
# Write 0xFF to register 0x00 - can misconfigure the chip
i2cset -y 1 0x40 0x00 0xFF
```

## Verifying INA228 Specifically

The `i2cdump` command is most useful for verification. The INA228 has specific registers at known addresses:

- **Register 0x00**: Configuration
- **Register 0x01**: ADC Configuration  
- **Register 0x04**: Shunt Voltage
- **Register 0x05**: Bus Voltage
- **Register 0x07**: Current

If `i2cdump -y 1 0x40` shows reasonable hex values (not all `FF` or all `00`), the chip is alive and responding.

## Quick Verification Steps

1. Run `i2cdetect -y 1` to confirm device address
2. Run `i2cdump -y 1 [address]` to verify chip is responding
3. Look for non-zero, non-FF values in the dump output


