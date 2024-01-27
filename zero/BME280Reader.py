import smbus2
import bme280
import time

class BME280Reader:
    def __init__(self):
        self.address = 0x77
        self.bus = smbus2.SMBus(1)
        self.calibration_params = bme280.load_calibration_params(self.bus,self.address)

    def get_values(self):
        # Read the raw data from the BME280
        data = bme280.sample(self.bus, self.address, self.calibration_params)
        temp = data.temperature
        pressure = data.pressure
        humidity = data.humidity
        
        return (temp,pressure,humidity)
    
# Use this to test the class
if __name__ == "__main__":
    my_bme = BME280Reader()
    while True:
        (temp,pressure,humidity) = my_bme.get_values()
        print(f'Temp: {temp}{chr(176)}C Humidity: {humidity}% Pressure: {pressure}hPa')
        time.sleep(1)
        
    
