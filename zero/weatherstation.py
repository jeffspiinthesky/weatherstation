import time
import smbus2
import bme280

address = 0x77

bus = smbus2.SMBus(1)

calibration_params = bme280.load_calibration_params(bus,address)

def celcius_to_fahrenheit(celcius):
        return (celcius * 9/5) + 32

def main():
        while True:
                try:
                        data = bme280.sample(bus, address, calibration_params)
                        temperature_celcius = data.temperature
                        pressure = data.pressure
                        humidity = data.humidity
                        temperature_fahrenheit = celcius_to_fahrenheit(temperature_celcius)

                        print('Temperature {:.2f}°C, {:.2f}°F'.format(temperature_celcius, temperature_fahrenheit))
                        print('Pressure {:.2f} hPa'.format(pressure))
                        print('Humidity: {:.2f}%'.format(humidity))
                        time.sleep(2)
                except KeyboardInterrupt:
                        print('Stopped')
                        break
                except Exception as e:
                        print('An unexpected error occurred: ', str(e))
                        break

if __name__ == "__main__":
        main()
