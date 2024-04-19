#!/usr/bin/env python3
import minimalmodbus 

k = minimalmodbus.Instrument('/dev/ttyUSB0', 1)
k.serial.baudrate = 9600

try:
    k.write_register(640, 6, 0, signed=False)
except minimalmodbus.NoResponseError:
    value = k.read_register(640, 0)
    if(6 == value):
        print('success')
        print(k.read_register(640, 0))
    else:
        print(k.read_register(640, 0))
        print('fail')

print(k.read_register(640, 0))
