from BME280Reader import BME280Reader
from colourcalc import ColourCalc
from flask import Flask, flash, request, Response, redirect, url_for, render_template
import json
import time

bme280_reader = BME280Reader()
colourcalc = ColourCalc()

app = Flask(__name__, instance_relative_config=True)

@app.route('/data',methods=['GET'])
def get_data():
    (year, month, mday, hour, minute, second, weekday, yearday, isdst) = time.localtime() # get struct_time
    time_string = f'{year}/{month:02}/{mday:02}-{hour:02}:{minute:02}:{second:02}'
    (temp,pressure,humidity) = bme280_reader.get_values()
    print(f'Temp: {temp:.2f} Humidity: {humidity:.2f} Pressure: {pressure:.2f}')
    #Derive colour to represent temperature
    (red, green, blue) = colourcalc.calc_colour(int(temp))
    #Template JSON
    data = f"""{{
"time": "{time_string}",
"temperature": "{temp}",
"tempcolour": "#{red:02x}{green:02x}{blue:02x}",
"pressure": "{pressure:.2f}",
"humidity": "{humidity:.2f}",
"wind_speed": "{0}"
}}"""
    bytes = json.dumps(data)
    return Response(data,mimetype='application/json')

@app.route('/', methods=['GET'])
def serve():
    return render_template('index.html')

# Use to test
if __name__ == "__main__":
    app.run()
