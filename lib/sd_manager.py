import machine
import sdcard
import time
import dht
import uos
from time import sleep
import os

class SDManager:
    def __init__(self, spi_id=1, sck=10, mosi=11, miso=12, cs=13, baudrate=1000000):
        """Init SPI bus and SD Card"""
        self.spi = machine.SPI(
            spi_id,
            baudrate=baudrate,
            polarity=0,
            phase=0,
            sck=machine.Pin(sck),
            mosi=machine.Pin(mosi),
            miso=machine.Pin(miso)
        )
        self.cs = machine.Pin(cs, machine.Pin.OUT)
        self.sd = None
        self.vfs = None
        
    def mount(self, mount_point="/sd"):
        """Mount SD Card"""
        try:
            self.sd = sdcard.SDCard(self.spi, self.cs)
            self.vfs = uos.VfsFat(self.sd)
            uos.mount(self.vfs, mount_point)
            print(f"SD Card mounted at {mount_point}")
        except Exception as e:
            print("Failed to mount SD Card: ", e)
            
    def write(self, text):
        """Write text to SD Card"""
        try:
            with open("/sd/log.txt", "a") as f:
                f.write(text)
                f.flush()
            print(f"Wrote data")
        except Exception as e:
            print("Error writing file: ", e)
    
    def umount(self, mount_point="/sd"):
        """Unmount the SD Card"""
        try:
            uos.umount(mount_point)
            print("Unmounted")
        except Exception as e:
            print("Failed to unmount: ", e)
            
            
class DHTManager:
    def __init__(self, gpio_pin):
        self.sensor = dht.DHT11(machine.Pin(gpio_pin))
        self._last_measure = 0
        self._temperature = None
        self._humidity = None
        
    def _ensure_measure(self):
        if time.ticks_diff(time.ticks_ms(), self._last_measure) >= 2000:
            try:
                self.sensor.measure()
                self._temperature = self.sensor.temperature()
                self._humidity = self.sensor.humidity()
                self._last_measure = time.ticks_ms()
                print("Measurement OK:", self._temperature, self._humidity)
            except OSError as e:
                print("DHT read failed:", e)
                
    def get_temp_c(self):
        self._ensure_measure()
        return str(self._temperature)
    
    def get_temp_f(self):
        self._ensure_measure()
        if self._temperature is None:
            return None
        return str(self._temperature * 9 / 5 + 32.0)
        
    def get_humidity(self):
        self._ensure_measure()
        return str(self._humidity)

    def get_date(self):
        UTC_OFFSET = -7 * 60 * 60
        year, month, day, hour, minute, second, _, _ = time.localtime(time.time() + UTC_OFFSET)
        return "DATE: {:02d}/{:02d}/{} at {:02d}:{:02d}:{:02d}".format(
            month, day, year, hour, minute, second
        )
    
    
        
