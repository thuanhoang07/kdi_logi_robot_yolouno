from machine import Pin, I2C
from utility import *
from setting import *
from micropython import const
import stm32_line

class LineSensor2:
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


class LineSensorI2C2(LineSensor2):
    def __init__(self, scl_pin2, sda_pin2, address=0x23):
        self.scl2 = scl_pin2
        self.sda2 = sda_pin2
        self.i2c_stm = machine.I2C(1, scl= self.scl2, sda= self.sda2, freq = 100000)
#         self.i2c_pcf = SoftI2C(scl=scl_pin, sda=sda_pin, freq=100000)
        self.address = address

        try:
            self.stm = stm32_line.STM32(self.i2c_stm, self.address)
        except:
            self.stm = None
            print('Line sensor not found')

    def read_ss2(self, index=None):
        # 0 white, 1 black
        if self.stm == None:
            return 0

        if index == None:
            return (self.stm.pin(0), self.stm.pin(1), self.stm.pin(2), self.stm.pin(3))

        return self.stm.pin(index)

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

