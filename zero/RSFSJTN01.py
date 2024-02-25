import RPi.GPIO as GPIO
from time import sleep
import threading

class RSFSJTN01():
    wind_speed = 0
    count = 0
    input_pin_number = 0
    input_pin = None
    done = False
    poll_thread = None
    thread_finished = False
    lock = threading.Lock()
    
    def __init__(self, input_pin_number):
        self.input_pin_number = input_pin_number
        GPIO.setmode(GPIO.BCM)
        self.input_pin = GPIO.setup(self.input_pin_number, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.input_pin_number, GPIO.RISING, callback=self.pulse_detected)
        self.poll_thread = threading.Thread(target=self.poll_thread, args=())
        print(f'Thread: {self.poll_thread}')
        self.poll_thread.start()
    
    def pulse_detected(self,p):
        #print(f'Pulse! {p}')
        self.count = self.count + 1
        
    def poll_thread(self):
        while (not self.done):
            self.set_wind_speed()
            self.reset_count()
            sleep(1)
        self.thread_finished = True
        print('Thread finished')
        
    def reset_count(self):
        print('Resetting')
        self.lock.acquire()
        self.count = 0
        self.lock.release()
        
    def set_wind_speed(self):
        self.lock.acquire()
       	print(f'Count: {self.count}')
       	## multiply counted pulses by 8.75cm/s and divide by number of secs since last calc
       	## then divide by 100 to get m/s and multiply by 2.23694 to get mph
       	self.wind_speed = (self.count * 0.0875) * 2.23694
        self.lock.release()
    
    def get_wind_speed(self):
        return self.wind_speed
    
    def end(self):
        self.done = True
        while self.poll_thread.is_alive():
            print("Waiting for thread to finish")
            self.poll_thread.join(timeout=1)
       
    
# This can be used to test the class. Spin up an instance and call it every second to get wind speed
if __name__ == "__main__":
    try:
        wind_speed_sensor = RSFSJTN01(21)
        while True:
            sleep(1)
            print(f'Returned wind speed: {wind_speed_sensor.get_wind_speed()}mph')
    except KeyboardInterrupt:
        wind_speed_sensor.end()
