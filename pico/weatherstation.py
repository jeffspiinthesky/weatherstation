#from RSFSJTN01 import RSFSJTN01
from BME280Reader_adafruit import BME280Reader
from NtpClient import NtpClient
from colourcalc import ColourCalc
from socket import socket
from time import localtime
from Wifi import Wifi
from machine import ADC
import os

class WeatherServer:
    def __init__(self, ntp_host, port, bme280_sda, bme280_scl, wind_speed_pin):
        # Set up temperature sensor
        adcpin = 4
        self.sensor = ADC(adcpin)
        # Connect to Wifi
        self.wifi_connection = Wifi()
        self.ip = self.wifi_connection.connect()
        # Set the time from the provided NTP server
        self.ntp_host = ntp_host
        self.ntp_client = NtpClient(self.ntp_host)
        self.ntp_client.set_time()
        # Set the listening port for incoming requests
        self.port = port
        # Set up the BME280
        self.bme280_sda = bme280_sda
        self.bme280_scl = bme280_scl
        self.bme280_reader = BME280Reader(self.bme280_sda, self.bme280_scl)
        self.colourcalc = ColourCalc()
        # Set up the wind speed detector
        self.wind_speed_pin = wind_speed_pin
        #self.wind_speed_sensor = RSFSJTN01(self.wind_speed_pin)
        # Set up the internal server
        address = (self.ip, self.port)
        self.connection = socket()
        self.connection.bind(address)
        self.connection.listen(1)
        
    def get_temperature(self):
        adc_value = self.sensor.read_u16()
        volt = (3.3/65535) * adc_value
        temperature = 27 - (volt - 0.706)/0.001721
        return round(temperature, 2)
    
    def get_data(self):
        pico_temp = self.get_temperature()
        pico_temp = 0
        (year, month, mday, hour, minute, second, weekday, yearday) = localtime() # get struct_time
        time_string = f'{year}/{month:02}/{mday:02}-{hour:02}:{minute:02}:{second:02}'
        (temp,pressure,humidity) = self.bme280_reader.get_values()
        #Derive colour to represent temperature
        (red, green, blue) = self.colourcalc.calc_colour(int(temp))
        #wind_speed = self.wind_speed_sensor.get_wind_speed()
        wind_speed = 0
        #Template JSON
        data = f"""{{
"pico_temperature": "{pico_temp}",
"time": "{time_string}",
"temperature": "{temp}",
"tempcolour": "#{red:02x}{green:02x}{blue:02x}",
"pressure": "{pressure}",
"humidity": "{humidity}",
"wind_speed": "{wind_speed}"
}}"""
        response = f"""HTTP/1.1 200 OK
Content-Type: application/json; encoding=utf8
Content-Length: {len(data)}
Access-Control-Allow-Origin: *

{data}"""
        print(response)
        return str(response)
    
    def send_file(self,filename,mime_type,client):
        size = os.stat(filename)[6]
        print(f'Stats: {size}')
        file = open(filename,'r')
        data = file.read()
        response = f"""HTTP/1.1 200 OK
Content-Type: {mime_type}; encoding=utf8
Content-Length: {size}
Access-Control-Allow-Origin: *

{data}"""
        print(response)
        client.send(response)        

    def serve(self):
        while True:
            print('Waiting for request')
            if( self.wifi_connection.is_connected() == False ):
                self.wifi_connection = Wifi()
                self.ip = self.wifi_connection.connect()
                address = (self.ip, self.port)
                self.connection = socket()
                self.connection.bind(address)
                self.connection.listen(1)
            print(self.connection)
            client = self.connection.accept()[0]
            print(client)
            request = client.recv(1024)
            request = str(request)
            print(request)
            try:
                request = request.split()[1]
                print(request)
                if request == '/data':
                    client.send(self.get_data())
                elif request == '/':
                    self.send_file('webpage/index.html','text/html',client)
                elif request == '/jquery.textfill.min.js':
                    self.send_file('webpage/jquery.textfill.min.js','text/javascript',client)
                elif request == '/weatherstation.css':
                    self.send_file('webpage/weatherstation.css','text/css',client)
                elif request == '/weatherstation.js':
                    self.send_file('webpage/weatherstation.js','text/javascript',client)
                else:
                    response = f"""HTTP/1.1 404 Not found"""
                    client.send(response)        
            except IndexError:
                pass
            print('Data sent - closing')
            client.close()
            print('Closed')
            
# Use to test
if __name__ == "__main__":
    try:
        weather_server = WeatherServer('pool.ntp.org', 80, 0, 1, 2)
        while True:
            weather_server.serve()
    except KeyboardInterrupt:
        machine.reset()