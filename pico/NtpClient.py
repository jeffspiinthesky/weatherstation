import network
from socket import socket,AF_INET,SOCK_DGRAM,getaddrinfo
from time import localtime,gmtime
from struct import unpack
from machine import RTC

class NtpClient:
    def __init__(self, ntp_host):
        self.host = ntp_host
        self.NTP_DELTA = 2208988800
        self.set_retries = 0
        
    def set_time(self):
        time_set = 0
        NTP_QUERY = bytearray(48)
        NTP_QUERY[0] = 0x1B
        addr = getaddrinfo(self.host, 123)[0][-1]
        while (time_set == 0) and (self.set_retries < 5):
            try:
                s = socket(AF_INET, SOCK_DGRAM)
                s.settimeout(5)
                res = s.sendto(NTP_QUERY, addr)
                msg = s.recv(48)
                val = unpack("!I", msg[40:44])[0]
                t = val - self.NTP_DELTA    
                tm = gmtime(t)
                RTC().datetime((tm[0], tm[1], tm[2], tm[6] + 1, tm[3], tm[4], tm[5], 0))
                time_set = 1
                self.set_retries = 0
            except Exception as e:
                print( "Error: %s" % e )
                time_set = 0
                self.set_retries = self.set_retries + 1
            finally:
                s.close()

if __name__ == "__main__":
    from Wifi import Wifi
    wifi_connection = Wifi()
    ip_address = wifi_connection.connect()
    print(f'Current time: {localtime()}')
    ntp_client = NtpClient('pool.ntp.org')
    ntp_client.set_time()
    print(f'Current time: {localtime()}')
    