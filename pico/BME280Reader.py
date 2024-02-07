import bme280
import time
from machine import Pin, I2C

class BME280Reader:
    def __init__(self, sda_pin, scl_pin):
        self.sda_pin = sda_pin
        self.scl_pin = scl_pin
        self.i2c=I2C(0,sda=Pin(self.sda_pin), scl=Pin(self.scl_pin), freq=400000)
        self.bme = bme280.BME280(i2c=self.i2c)
        
    def get_values(self):
        # Read the raw data from the BME280
        t, p, h = self.bme.read_compensated_data()
        temp = t / 100
    
        p = p // 256
        pi = p // 100
        pd = p - pi * 100
        pressure = pi + (pd / 100)
        
        hi = h // 1024
        hd = h * 100 // 1024 - hi * 100
        humidity = hi + (hd / 100)
        
        return (temp,pressure,humidity)
    
# Use this to test the class
if __name__ == "__main__":
    my_bme = BME280Reader(0,1)
    while True:
        (temp,pressure,humidity) = my_bme.get_values()
        print(f'Temp: {temp}{chr(176)}C Humidity: {humidity}% Pressure: {pressure}hPa')
        time.sleep(1)
        
    