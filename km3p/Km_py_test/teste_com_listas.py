#!/usr/bin/env python3
import minimalmodbus

config = {
    'measured value':[0, 1, 0, 0, False], #'key' : [writable?(0 = r, 1 = w, 3 = r/w), address, value,decimal_point, singed]
    'number of setpoints':[3, 740, 1, 0, False], #values = 1-4
    'select setpoint':[3, 5, 0, 0, False], #0-3
    'setpoint range':[3, 6, 0, 0, False], #address: 6-9; SPLL<values<SPLH
    'sensor type':[3, 640, 7, 0, False] # 7 = pt100
}

def write_reg(instrument:minimalmodbus.Instrument, val:dict):
    try:
        instrument.write_register(val[1],val[2], val[3], signed=val[4])
    except minimalmodbus.NoResponseError:
        pass

def reset_to_default(instrument:minimalmodbus.Instrument):
    r = write_reg(instrument, [3, 19, -481, 0, True])
    if(r):
        print('success')
    else:
        print('failed')

km3 = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
km3.serial.baudrate = 9600
km3.write_register(640, 7, 0)
# reset_to_default(km3)
# write_register(km3, config('sensor type'))
print(km3.read_register(1))

