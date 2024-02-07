from machine import Pin
import time
import _thread

class RSFSJTN01:
    def __init__(self, input_pin_number):
        self.wind_speed = 0
        self.count = 0
        self.input_pin_number = input_pin_number
        self.last_time=time.time_ns()
        self.input_pin = Pin(self.input_pin_number, Pin.IN, Pin.PULL_UP)
        self.input_pin.irq(trigger=Pin.IRQ_RISING, handler=self.pulse_detected)
    
    def pulse_detected(self,p):
        print(f'Pulse! {p}')
        self.count = self.count + 1

    def get_wind_speed(self):
        curr_time_ns = time.time_ns()
        # convert ns to s
        time_delta = (curr_time_ns - self.last_time) / 1000000000.0
        # If there has been less than a second between now and the prior
        # request, just return the previous wind speed. Otherwise
        # you'll just get a divide by zero exception if you get
        # multiple requests in
        if time_delta == 0:
            return self.wind_speed
        # multiply counted pulses by 8.75cm/s and divide by number of secs since last calc
        # then divide by 100 to get m/s and multiply by 2.23694 to get mph
        self.wind_speed = (((self.count * 8.75) / time_delta ) / 100) * 2.23694
        self.count = 0
        self.last_time = curr_time_ns
        return self.wind_speed
    
# This can be used to test the class. Spin up an instance and call it every second to get wind speed
if __name__ == "__main__":
    device = RSFSJTN01(2)
    while True:
        time.sleep(1)
        print(f'Returned wind speed: {device.get_wind_speed()}mph')
