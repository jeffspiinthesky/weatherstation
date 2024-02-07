from adafruit_bme280 import basic as adafruit_bme280
from busio import I2C
from microcontroller import pin
from time import sleep

class BME280Reader:    
    def __init__(self, sda_pin, scl_pin):
        self.__pins = [
        pin.GP0,
        pin.GP1,
        pin.GP2,
        pin.GP3,
        pin.GP4,
        pin.GP5,
        pin.GP6,
        pin.GP7,
        pin.GP8,
        pin.GP9,
        pin.GP10,
        pin.GP11,
        pin.GP12,
        pin.GP13,
        pin.GP14,
        pin.GP15,
        pin.GP16,
        pin.GP17,
        pin.GP18,
        pin.GP19,
        pin.GP20,
        pin.GP21,
        pin.GP22,
        pin.GP23,
        pin.GP24,
        pin.GP25,
        pin.GP26,
        pin.GP27,
        pin.GP28,
        pin.GP29]
        self.sda_pin = self.__pins[sda_pin]
        self.scl_pin = self.__pins[scl_pin]
        i2c = I2C(self.scl_pin, self.sda_pin)  # SCL, SDA
        self.bme280 = adafruit_bme280.Adafruit_BME280_I2C(i2c)
        
    def get_values(self):
        t = self.bme280.temperature
        h = self.bme280.humidity
        p = self.bme280.pressure
        temp = t
        pressure = p
        humidity = h
        
        return (temp,pressure,humidity)
    
# Use this to test the class
if __name__ == "__main__":
    my_bme = BME280Reader(0,1)
    while True:
        (temp,pressure,humidity) = my_bme.get_values()
        print(f'Temp: {temp:.02f}{chr(176)}C Humidity: {humidity:.02f}% Pressure: {pressure:.02f}hPa')
        time.sleep(1)
        
    