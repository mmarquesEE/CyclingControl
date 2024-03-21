import pyvisa
from dischargeCC import setDischargeConst

#Conexion

rm = pyvisa.ResourceManager()

try:
    v = rm.open_resource('USB0::0x2A8D::0x3902::MY61001566::INSTR')
except Exception as e:
    print("Check if your device is connected!!")

#Modes: CC or CP
#setDischargeCC(v, mode, channel, curr, cfVolt, cfVoltParam, cfCap, cfCapParam)

setDischargeConst(v, 'CURR', 1 , 1.3 , 'VOLT', 9 , 'CAP', 1.04)



