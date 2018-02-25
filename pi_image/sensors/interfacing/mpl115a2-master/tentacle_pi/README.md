# Tentacle Pi

[![PyPI](https://img.shields.io/pypi/v/tentacle_pi.svg)]()

WARNING for Tentacle Pi 1.0.0 release:

 * Tentacle Pi will be released under the GPLv2
 * Drivers are rewritten in pure python (new API)

Tentacle Pi is a growing collection of drivers for popular I2C devices.


## Supported I2C devices

| I2C device    | Address       | Sensor type   | Spec sheet |
| ------------- |:-------------:|:-------------:|:-----------|
| am2315        | 0x5c          | Temperature/Humidity |  [Link](https://www.adafruit.com/datasheets/AM2315.pdf) |
| am2321        | 0x5c          | Temperature/Humidity |  [Link](http://akizukidenshi.com/download/ds/aosong/AM2321_e.pdf) |
| bmp180        | 0x77          | Barometric Pressure/Temperature/Altitude |  [Link](http://www.adafruit.com/datasheets/BST-BMP180-DS000-09.pdf) |
| tsl2561       | 0x29,0x39,0x49| Luminosity/Lux/Light |  [Link](http://www.adafruit.com/datasheets/TSL2561.pdf) |
| mcp9808       | 0x18          | Temperature |  [Link](http://www.farnell.com/datasheets/1522173.pdf) |
| mpl115a2      | 0x60          | Barometric Pressure/Temperature |  [Link](http://cache.freescale.com/files/sensors/doc/data_sheet/MPL115A2.pdf) |
| lm75      	| 0x48          | Temperature |  [Link](http://datasheets.maximintegrated.com/en/ds/LM75.pdf) |


Remarks:

 * tsl2561: default address is 0x39
 * am2315/am2321: you can use the am2315 driver for am2321 sensor

## Supported platforms

Any arm powered single-board computer that runs a debian operating system is more or less supported.

Tested platforms so far are:

 * Raspberry Pi / Raspbian
 * Raspberry Pi 2 / Raspbian
 * Banana Pi / Raspbian
 * Odroid C1 / Ubuntu


## Installation
Install the following packages:

```bash
sudo apt-get install i2c-tools libi2c-dev python-dev build-essential
```

### I2C Configuration

#### Raspberry Pi 1 / 2
On the [Adafruit learning platform](https://learn.adafruit.com/) you will find a great tutorial
[how to configure I2C](https://learn.adafruit.com/adafruits-raspberry-pi-lesson-4-gpio-setup/configuring-i2c).
Besides that their products (AM2315, BMP180, TSL2561) are great :smile_cat: .

#### Odroid C1
Here is a great [blog post](https://www.abelectronics.co.uk/i2codroidc1/info.aspx) that explains how I2C can be configured on the Odroid C1.


### pip installer

```bash
sudo pip install tentacle_pi
```

If you want to update:

```bash
sudo pip install tentacle_pi --upgrade
```

### from source
Clone this repository:

```bash
git clone --recursive https://github.com/lexruee/tentacle_pi
```

Install the python module:

```bash
sudo python setup.py install
```

If you have already a copy of this repository you can run this command to update your local copy:

```bash
git pull origin master
git submodule update --init --recursive
```


## Usage
Raspberry Pi: add pi to the group i2c if you want to run your program without sudo.
```
sudo usermod -a -G i2c pi
```

### AM2315 / AM2321

Remark: You can also use the
AM2315 driver for AM2321 sensor.


```python

import time
from tentacle_pi.AM2315 import AM2315
am = AM2315(0x5c,"/dev/i2c-1")

for x in range(0,10):
	temperature, humidity, crc_check = am.sense()
	print "temperature: %0.1f" % temperature
	print "humidity: %0.1f" % humidity
	print "crc: %s" % crc_check
	print
	time.sleep(2)


```

### BMP180

```python
from tentacle_pi.BMP180 import BMP180
import time
bmp = BMP180(0x77,"/dev/i2c-1")


for x in range(0,10):
        print "temperature: %0.1f" % bmp.temperature()
        print "pressure: %s" % bmp.pressure()
        print "altitude: %0.1f" % bmp.altitude()
        print
        time.sleep(2)

```


### TSL2561

```python
from tentacle_pi.TSL2561 import TSL2561
import time

tsl = TSL2561(0x39,"/dev/i2c-1")
tsl.enable_autogain()
tsl.set_time(0x00)

for x in range(0,10):
	print "lux %s" % tsl.lux()
	print
	time.sleep(3)

```

### MCP9808

```python
import time
from tentacle_pi.MCP9808 import MCP9808
mcp = MCP9808(0x18,"/dev/i2c-1")

for x in range(0,10):
        temperature = mcp.temperature()
        print "temperature: %0.2f" % temperature
        time.sleep(2)


```

### MPL115A2

```python
import time
from tentacle_pi.MPL115A2 import MPL115A2
mpl = MPL115A2(0x60,"/dev/i2c-1")

for x in range(0,10):
    temperature, pressure = mpl.temperature(), mpl.pressure()
    print "temperature: %0.1f" % temperature
    print "pressure: %0.1f" % pressure
    print
    time.sleep(2)


```

### LM75

```python
import time
from tentacle_pi.LM75 import LM75
lm = LM75(0x48,"/dev/i2c-1")

for x in range(0,10):
        temperature = lm.temperature()
        print "temperature: %0.2f" % temperature
        time.sleep(2)


```

## Example: A simple CLI weather station

```python
from tentacle_pi.TSL2561 import TSL2561
from tentacle_pi.BMP180 import BMP180
from tentacle_pi.AM2315 import AM2315
import time
from datetime import datetime

# initialize some sensors :-)
bmp = BMP180(0x77, "/dev/i2c-1")
tsl = TSL2561(0x39, "/dev/i2c-1")
am = AM2315(0x5c, "/dev/i2c-1")

tsl.enable_autogain()

print("---------------------------------------------")
print("time: %s" % datetime.now())
print("")
print("bmp180:")
print("\ttemperature: %0.1f" % bmp.temperature())
print("\tpressure: %0.1f" % bmp.pressure())
print("\taltitude: %0.1f" % bmp.altitude())

print("tsl2561:")
print("\tlux: %s" % tsl.lux())

print("am2315:")
am_tmp, am_hum, _ = am.sense()
print("\ttemperature: %0.1f" % am_tmp)
print("\thumidity: %0.1f" % am_hum)
print("---------------------------------------------")
print("")
# use time.sleep(2) inside a loop because of the AM2315 sensor!

```

## Dependencies

* i2c-tools
* build-essential
* libi2c-dev
* python-dev
* python 2.7


## Changelog
 [Click here](https://github.com/lexruee/tentacle_pi/master/CHANGElOG.md)

## Copyright & License
```
The MIT License (MIT)

Copyright (c) 2015 Alexander Rüedlinger <a.rueedlinger@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```
