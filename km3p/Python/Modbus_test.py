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
    set_point1 = reg(6, 0)
    sensor_type = reg(640, 7)  

    alarm_1_type = reg(666, 4)  #type 4 = iterval low<=al<=high
    alarm_1_func = reg(667, 5)#1+4  # não inicia quando alimentado +1; +2 reset manual; +4 acknowledge; +8 mantem on fora do intervalo  
    alarm_1_high = reg(668) #high value
    alarm_1_low = reg(669) #low value

    out_3_func = reg(10260, 3) #digital output; 3 = alarm output
    out_3_alarm = reg(661, 1) #+1 Alarm;+2 Alarm 2;+4 Alarm 3;+8 Loop break alarm;+16 Sensor Break;+32 Overload on output 4

    km3p = minimalmodbus.Instrument(serial_port, slave_address)
    
    # params = []
    reset_default = reg(19, val=-481, sign=True)
    
    def __init__(self):
        self.km3p.serial.baudrate = self.baud_rate

    if __name__== '__main__':
        pass
    
    def set_alarm(self, set_point:int, faixa:int):
        self.alarm_1_high.value = faixa+set_point
        self.alarm_1_low.value = faixa-set_point
        self.write_reg(self.alarm_1_type, self.alarm_1_type.value )
        self.write_reg(self.alarm_1_func, self.alarm_1_func.value )
        self.write_reg(self.alarm_1_high, self.alarm_1_high.value )
        self.write_reg(self.alarm_1_low, self.alarm_1_low.value )
        self.write_reg(self.out_3_func, self.out_3_func.value )
        self.write_reg(self.out_3_alarm, self.out_3_alarm.value )

    def set_temperature(self, value=0):
        self.set_point1.value = value
        self.write_reg(self.set_point1, self.set_point1.value)

    def wait_temperature(self):
        if(self.read_reg(self.measure_value) != self.set_point1.value):
            return False
        return True

    def reset(self):
        self.write_reg(self.reset_default, self.reset_default.value, self.reset_default, self.reset_default.singed)

    def read_reg(self, register:reg):
        value = self.km3p.read_register(register.address, register.dec_point, signed=register.singed)
        return value 

    def write_reg(self, register:reg, value, signed=False):
        try:
            self.km3p.write_register(register.address, value, register.dec_point, signed=signed)
        except minimalmodbus.NoResponseError:
            pass
            # m = self.km3p.read_register(register.address, register.dec_point)
            # if(m == value):
            #     print(f'{namestr(register, globals())} has failed to write')
            # else:
            #     print(f'{namestr(register, globals())} has succeeded to write')


# def namestr(obj, namespace):
#     return [name for name in namespace if namespace[name] is obj]

km = km3()

# km.write_reg(km.set_point1.address, 60)
km.set_temperature(value=20)
# print(km.read_reg(km.measure_value))
# print(km.read_reg(km.select_set_point))
# a = km.km3p.read_register(1)
# print(a)
km.set_alarm(20, 2)
