#!/bin/bash
set -e
tar xvfz Adafruit_Blinka-*.tar.gz
tar xvfz Adafruit_Python_PlatformDetect*.tar.gz
unzip adafruit-circuitpython-bundle-*.zip
mkdir -p adafruit_blinka
mkdir -p adafruit_blinka/agnostic
mkdir -p adafruit_blinka/microcontroller
mkdir -p adafruit_blinka/microcontroller/rp2040
mkdir -p adafruit_blinka/microcontroller/generic_micropython
mkdir -p adafruit_blinka/board/raspberrypi
mkdir -p adafruit_bme280
mkdir -p generic_micropython
mkdir -p microcontroller/rp2040
mkdir -p adafruit_platformdetect/constants
mkdir -p adafruit_bus_device

# OK, lets sort out the root directory first. We need
# board.py
# busio.py
# digitalio.py

cp Adafruit_Blinka-*/src/board.py ./
cp Adafruit_Blinka-*/src/busio.py ./
cp Adafruit_Blinka-*/src/digitalio.py ./

# Next lets dig into the adafruit-blinka directory. We need
# __init__.py
# So that should be easy
cp Adafruit_Blinka-*/src/adafruit_blinka/__init__.py adafruit_blinka/

# Next lets dig into the agnostic directory. We need
# time.py
# __init__.py
cp Adafruit_Blinka-*/src/adafruit_blinka/agnostic/time.py ./adafruit_blinka/agnostic
cp Adafruit_Blinka-*/src/adafruit_blinka/agnostic/__init__.py ./adafruit_blinka/agnostic

# Now we need the board stuff from blinka
# board/__init__.py
# board/raspberrypi/__init__.py
# board/raspberrypi/pico.py
cp Adafruit_Blinka-*/src/adafruit_blinka/board/__init__.py ./adafruit_blinka/board/
cp Adafruit_Blinka-*/src/adafruit_blinka/board/raspberrypi/__init__.py ./adafruit_blinka/board/raspberrypi/
cp Adafruit_Blinka-*/src/adafruit_blinka/board/raspberrypi/pico.py ./adafruit_blinka/board/raspberrypi/

# Now we need the Blinka microcontroller code
# __init__.py
# pin.py
cp Adafruit_Blinka-*/src/microcontroller/* ./microcontroller/


# Now need to pull for the rp2040 chip (pico)
cp Adafruit_Blinka-*/src/adafruit_blinka/microcontroller/rp2040/i2c.py ./adafruit_blinka/microcontroller/rp2040/
cp Adafruit_Blinka-*/src/adafruit_blinka/microcontroller/rp2040/pin.py ./adafruit_blinka/microcontroller/rp2040/
cp Adafruit_Blinka-*/src/adafruit_blinka/microcontroller/rp2040/spi.py ./adafruit_blinka/microcontroller/rp2040/
cp Adafruit_Blinka-*/src/adafruit_blinka/microcontroller/rp2040/uart.py ./adafruit_blinka/microcontroller/rp2040/
cp Adafruit_Blinka-*/src/adafruit_blinka/microcontroller/rp2040/__init__.py ./adafruit_blinka/microcontroller/rp2040/

# Now for the adafruit_bme280 stuff. We need
# advanced.py
# basic.py
# __init__.py
# protocol.py
# These are the only files in the Adafruit circuitpython libs for bme280 so copying is easy
cp adafruit-circuitpython-bundle-*/lib/adafruit_bme280/* adafruit_bme280/

# Next is the generic_micropython directory. We need
# i2c.py  
# __init__.py  
# spi.py
# Like with the last files, these are the only files in the Adafruit_Blinka-8.31.0/src/adafruit_blinka/microcontroller/generic_micropython so we can copy the lot in one go
cp Adafruit_Blinka-*/src/adafruit_blinka/microcontroller/generic_micropython/* ./adafruit_blinka/microcontroller/generic_micropython/

# Next is the platformdetect directory. We need
# board.py  
# chip.py   
# __init__.py  
# revcodes.py
# constants/boards.py
# constants/chips.py
# constants/__init__.py
# So we can just do a recursive copy
cp -R Adafruit_Python_PlatformDetect-*/adafruit_platformdetect/* ./adafruit_platformdetect/

# Finally there's the adafruit_bus_device directory. We need
# i2c_device.py
# __init__.py
# spi_device.py
# Which again is everything in the source directory so we can do a wildcard copy
cp adafruit-circuitpython-bundle-*/lib/adafruit_bus_device/* adafruit_bus_device/

# That's everything. Now we can clean up
rm -f Adafruit_Blinka-*.tar.gz
rm -f Adafruit_Python_PlatformDetect*.tar.gz
rm -f adafruit-circuitpython-bundle-*.zip
rm -rf Adafruit_Blinka-*
rm -rf adafruit-circuitpython-bundle-*
rm -rf Adafruit_Python_PlatformDetect-*

# That's all folks!!
exit 0
