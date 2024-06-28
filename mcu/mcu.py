import serial
import time


class MCU:
    def __init__(self,com_port="COM3",baud=9600):
        self.serial = serial.Serial(com_port,baud)

    def close(self):
        self.serial.close()
    
    def is_open(self) -> bool:
        return self.serial.is_open
    
    def query_alarm(self,equip:str) -> bool:
        if equip in ['TC','DCL']:
            self.serial.write(f',{equip}_ALARM?,'.encode())
            resposta = self.serial.readline().decode().strip()

            if resposta == f"{equip}_ALARM ON":
                return True
            elif resposta == f"{equip}_ALARM OFF":
                return False
        else:
            return False
        
    def reset_eis(self,eis_ch:int):
        self.serial.write(f',RESET_EIS{eis_ch},'.encode())

    def cycler(self,onoff:bool):
        self.serial.write(f',CHARGE {"ON" if onoff else "OFF"},'.encode())
    
    def dcl_eis(self,onoff:bool):
        self.serial.write(f',DCL_EIS {"ON" if onoff else "OFF"},'.encode())
