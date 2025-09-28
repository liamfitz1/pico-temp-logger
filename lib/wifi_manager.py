import network
import time

class WifiManager:
    def __init__(self, ssid, password, retries=10, delay=2):
        self.ssid = ssid
        self.password = password
        self.retries = retries
        self.delay = delay
        self.wlan = network.WLAN(network.STA_IF)
        self.wlan.active(True)
        
    def connect(self):
        if not self.wlan.isconnected():
            print(f"Connecting to {self.ssid}")
            self.wlan.connect(self.ssid, self.password)
            
            for i in range(self.retries):
                if self.wlan.isconnected():
                    break
                print(f"Waiting for connection...{i}")
                time.sleep(self.delay)
            
            if self.wlan.isconnected():
                print("Connected!")
                return True
            else:
                print("Error connecting")
                return False
                
    def disconnect(self):
        if self.wlan.isconnected():
            self.wlan.disconnect()
            print("Disconnected")
            
    def is_connected(self):
        return self.wlan.isconnected()
        
    def ip_config(self):
        if self.wlan.isconnected():
            return self.wlan.ifconfig()
        return None