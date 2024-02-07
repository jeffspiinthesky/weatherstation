import time
import smbus2
import bme280

address = 0x77

bus = smbus2.SMBus(1)

calibration_params = bme280.load_calibration_params(bus,address)

def main():
        while True:
                data = bme280.sample(bus, address, calibration_params)
                temperature_celcius = data.temperature
                pressure = data.pressure
                humidity = data.humidity

                print(f'Temperature {temperature_celcius:.2f}°C')
                print(f'Pressure {pressure:.2f} hPa')
                print(f'Humidity: {humidity:.2f}%')
                time.sleep(2)

if __name__ == "__main__":
        main()
