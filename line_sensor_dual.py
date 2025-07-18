from machine import Pin, SoftI2C
from utility import *
from setting import *
from micropython import const
import pcf8574_dual

class LineSensor:
    def __init__(self):
        pass

    '''
        Chheck robot position according to line
            -2: too much to the left 
            -1: to the left 
            0: on track 
            1: to the right 
            2: too much to the right
    '''
    def check(self): 
        return 0

    '''
        Read status of a specific sensor
    '''
    def read(self, index=None):    
        return 0


class LineSensor2P(LineSensor):
    def __init__(self, s1, s2):
        self._s1 = Pin(s1, Pin.IN)
        self._s2 = Pin(s2, Pin.IN)
        super().__init__()

    '''
        Check robot position according to line
            -2: too much to the left 
            -1: to the left 
            0: on track 
            1: to the right 
            2: too much to the right
    '''
    def check(self):
        state = self.read()
        if state == (0, 0):
            return LINE_CENTER
        elif state == (0, 1):
            return LINE_LEFT2
        elif state == (1, 0):
            return LINE_RIGHT2
        else:
            return LINE_CROSS

    '''
        Read status of a specific sensor
    '''
    def read(self, index=None):
        if index == 0:
            return self._s1.value()
        elif index == 1:
            return self._s2.value()
        else:
            return (self._s1.value(), self._s2.value())

class LineSensor3P:
    def __init__(self, s1, s2, s3):
        self._s1 = Pin(s1, Pin.IN)
        self._s2 = Pin(s2, Pin.IN)
        self._s3 = Pin(s3, Pin.IN)
        super().__init__()

    '''
        Check robot position according to line
            -2: too much to the left 
            -1: to the left 
            0: on track 
            1: to the right 
            2: too much to the right
    '''
    def check(self):
        state = self.read()
        if state == (1, 1, 1):
            return LINE_CROSS
        elif state == (0, 0, 0):
            return LINE_END
        elif state == (1, 1, 0):
            return LINE_RIGHT
        elif state == (0, 1, 1):
            return LINE_LEFT
        elif state == (1, 0, 0):
            return LINE_RIGHT2
        elif state == (0, 0, 1):
            return LINE_LEFT2
        else:
            return LINE_CENTER

    '''
        Read status of a specific sensor
    '''
    def read(self, index=None):
        if index == 0:
            return self._s1.value()
        elif index == 1:
            return self._s2.value()
        else:
            return (self._s1.value(), self._s2.value())


class LineSensorI2C(LineSensor):
    def __init__(self, scl_pin = SCL_PIN , sda_pin = SDA_PIN, address=0x23):
        self.scl = scl_pin
        self.sda = sda_pin
        self.i2c_pcf = SoftI2C(scl=self.scl, sda=self.sda, freq = 100000)
#         self.i2c_pcf = SoftI2C(scl=scl_pin, sda=sda_pin, freq=100000)
        self.address = address

        try:
            self.pcf = pcf8574_dual.PCF8574_dual(self.i2c_pcf, self.address)
        except:
            self.pcf = None
            print('Line sensor not found')

    def read(self, index=None):
        # 0 white, 1 black
        if self.pcf == None:
            return 0

        if index == None:
            return (self.pcf.pin(0), self.pcf.pin(1), self.pcf.pin(2), self.pcf.pin(3))

        return self.pcf.pin(index)

    '''
        Check robot position according to line
            -2: too much to the left 
            -1: to the left 
            0: on track 
            1: to the right 
            2: too much to the right
    '''
    def check(self): 
        now = self.read()
        #print(now)
        if now == (0, 0, 0, 0):
            return LINE_END
        elif now == (1, 1, 1, 1):
            return LINE_CROSS
        elif (now[1], now[2]) == (1, 1) or now == (1, 0, 0, 1):
            return LINE_CENTER
        elif (now[0], now[1]) == (1, 1): 
            return LINE_RIGHT2
        elif (now[2], now[3]) == (1, 1): 
            return LINE_LEFT2
        elif now == (0, 0, 1, 0): 
            return LINE_RIGHT
        elif now == (0, 1, 0, 0): 
            return LINE_LEFT
        elif now[1] == 1: 
            return LINE_RIGHT2
        elif now[2] == 1:
            return LINE_LEFT2
        elif now[0] == 1: 
            return LINE_RIGHT3
        elif now[3] == 1: 
            return LINE_LEFT3
        
        
class LineSensor2I2C(LineSensor):
    def __init__(self, scl_pin2 , sda_pin2, address=0x23):
        self.scl2 = scl_pin2
        self.sda2 = sda_pin2
        self.i2c_pcf2 = I2C(0, scl=self.scl2, sda=self.sda2, freq = 100000)
#         self.i2c_pcf = SoftI2C(scl=scl_pin, sda=sda_pin, freq=100000)
        self.address = address

        try:
            self.pcf2 = pcf8574_dual.PCF8574_dual(self.i2c_pcf2, self.address)
        except:
            self.pcf2 = None
            print('Line sensor not found')

    def read_ss2(self, index=None):
        # 0 white, 1 black
        if self.pcf2 == None:
            return 0

        if index == None:
            return (self.pcf2.pin(0), self.pcf2.pin(1), self.pcf2.pin(2), self.pcf2.pin(3))

        return self.pcf2.pin(index)

    '''
        Check robot position according to line
            -2: too much to the left 
            -1: to the left 
            0: on track 
            1: to the right 
            2: too much to the right
    '''
    def check_ss2(self): 
        now = self.read_ss2()
        #print(now)
        if now == (0, 0, 0, 0):
            return LINE_END
        elif now == (1, 1, 1, 1):
            return LINE_CROSS
        elif (now[1], now[2]) == (1, 1) or now == (1, 0, 0, 1):
            return LINE_CENTER
        elif (now[0], now[1]) == (1, 1): 
            return LINE_RIGHT2
        elif (now[2], now[3]) == (1, 1): 
            return LINE_LEFT2
        elif now == (0, 0, 1, 0): 
            return LINE_RIGHT
        elif now == (0, 1, 0, 0): 
            return LINE_LEFT
        elif now[1] == 1: 
            return LINE_RIGHT2
        elif now[2] == 1:
            return LINE_LEFT2
        elif now[0] == 1: 
            return LINE_RIGHT3
        elif now[3] == 1: 
            return LINE_LEFT3
