from wifi_manager import WifiManager
from sd_manager import SDManager, DHTManager
import ntptime, network, time, os
import secrets

UTC_OFFSET = -7 * 60 * 60

def blink(t, c):
    for x in range(0,c):
        led.value(0)
        time.sleep_ms(t)
        led.value(1)
        time.sleep_ms(t)
    time.sleep(2)

sd = SDManager(baudrate=1000000)
dhtm = DHTManager(gpio_pin=15)
led = machine.Pin("LED", machine.Pin.OUT)

blink(100, 3)

wifi = WifiManager(secrets.ssid, secrets.password)
wifi.connect()

if wifi.is_connected():
    print(f"IP Address: {wifi.ip_config()[0]}")
    blink(100, 4)
    

counter = 0
while True:
    try:
        ntptime.settime()
        actual_time = time.localtime(time.time() + UTC_OFFSET)
        print(f"ACTUAL TIME: {str(actual_time)}")
        blink(100,5)
        break
    except OSError as e:
        time.sleep(1)

sd.mount()

try:
    while True:
        sd.write(dhtm.get_date() + "\r\n")
        print(dhtm.get_date())
        sd.write(dhtm.get_temp_c() + "C\r\n")
        sd.write(dhtm.get_temp_f() + "F\r\n")
        sd.write(dhtm.get_humidity() + "\r\n")
        actual_time = time.localtime(time.time() + UTC_OFFSET)
        sd.write(f"ACTUAL TIME: {actual_time}\r\n")
        print(f"ACTUAL TIME: {actual_time}\r\n")
        sd.write(f"COUNTER: {counter}\r\n")
        print(f"COUNTER: {counter}\r\n")
        counter += 1
        blink(100,5)
        time.sleep(30)
except KeyboardInterrupt:
    print("Keyboard interrupt.")
    
sd.umount()
