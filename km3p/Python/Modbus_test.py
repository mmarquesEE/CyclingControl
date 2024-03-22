#!/usr/bin/env python3
import minimalmodbus

class reg:
    address = int
    value = int
    dec_point = int
    singed = bool

    def __init__(self, add, val=0, dp=0, sign = False):
        self.address = add
        self.value = val
        self.dec_point = dp
        self.singed = sign

class km3:
    slave_address = 1
    baud_rate = 9600
    serial_port = '/dev/ttyUSB0'

    measure_value = reg(1)    
    select_set_point = reg(5)
    current_set_point = reg(2)
    sensor_type = reg(640, 7)    

    km3p = minimalmodbus.Instrument(serial_port, slave_address)
    
    # params = []
    reset_default = reg(19, val=-481, sign=True)
    
    def __init__(self):
        self.km3p.serial.baudrate = self.baud_rate

    if __name__== '__main__':
        pass
    
    def set_setpoint(self, setpoint:int, value=0):
        # self.write_reg()
        pass

    def reset(self):
        self.write_reg(self.reset_default, self.reset_default.value, self.reset_default, self.reset_default.singed)

    def read_reg(self, register:reg):
        value = self.km3p.read_register(register.address, register.dec_point, signed=register.singed)
        return value 

    def write_reg(self, register:reg, value, signed=False):
        try:
            self.km3p.write_register(register.address, value, register.dec_point, signed=signed)
        except minimalmodbus.NoResponseError:
            m = self.km3p.read_register(register.address, register.dec_point)
            if(m == value):
                print(f'{namestr(register, globals())} has failed to write')
            else:
                print(f'{namestr(register, globals())} has succeeded to write')


def namestr(obj, namespace):
    return [name for name in namespace if namespace[name] is obj]

km = km3()


km.write_reg(km.sensor_type, km.sensor_type.value)
# print(km.read_reg(km, km.measure_value))
# print(km.read_reg(km.select_set_point))
# a = km.km3p.read_register(1)
# print(a)

