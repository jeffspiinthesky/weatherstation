from weatherstation import WeatherServer

if __name__ == "__main__":
    try:
        weather_server = WeatherServer('pool.ntp.org', 80, 0, 1, 2)
        while True:
            weather_server.serve()
    except KeyboardInterrupt:
        machine.reset()