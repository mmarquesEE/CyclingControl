#!/usr/bin/env python3
import minimalmodbus
class reg:
    address:int
    value:int
    dec_point:int
    singed:bool

    def __init__(self, add, val=0, dp=0,sign = False):
        self.address = add
        self.value = val
        self.dec_point = dp
        self.singed = sign

class km3:
    #presets
    dec = 0
    baud = reg(770, dp=dec)
    decimal = reg(641, dec, dp=0, sign=False)
    #mesurments and setpoints
    measure_value = reg(1, dec)    
    select_set_point = reg(5)
    current_set_point = reg(3, dp=dec)
    set_point1 = reg(6, 0, dec, sign=True)
    sensor_type = reg(640, 7)
    potency = reg(4, dp=2) 
    #pid
    tune_type = reg(695, 3, sign=False)
    tune_onoff = reg(696, 0)
    proportional = reg(700, dp=dec)
    integral = reg(701)
    derivative = reg(702)
    #alarms
    alarm_1_type = reg(666, 4)  #type 4 = iterval low<=al<=high
    alarm_1_func = reg(667, 5)#1+4  # não inicia quando alimentado +1; +2 reset manual; +4 acknowledge; +8 mantem on fora do intervalo  
    alarm_1_high = reg(668, 0, dec, sign=True) #high value
    alarm_1_low = reg(669, 0, dec, sign=True) #low value
    #outputs
    out_3_func = reg(660, 3) #digital output; 3 = alarm output
    out_3_alarm = reg(661, 1) #+1 Alarm;+2 Alarm 2;+4 Alarm 3;+8 Loop break alarm;+16 Sensor Break;+32 Overload on output 4

    km3p:minimalmodbus.Instrument
    #reset to standart values
    reset_default = reg(19, val=-481, sign=True)
    
    def __init__(self,slave_address=1,serial_port='/dev/ttyUSB0', timeout=0.25,baud_rate=9600, decimal=0,debug=False): #init
        self.km3p = minimalmodbus.Instrument(serial_port, slave_address, debug=debug)
        self.km3p.serial.baudrate = baud_rate
        self.km3p.serial.timeout = timeout
        self.write(self.tune_type)
        decimal = 1 if (decimal > 0 & decimal < 2) else 0
        self.decimal.value = decimal
        self.dec = decimal
        self.write(self.decimal)
        

    def write(self, reg:reg): #escreve no registrador, função fundamental
        #modbus function 6 = write single register
        self.km3p.write_register(reg.address, reg.value, reg.dec_point, 6, reg.singed)

    def read(self, reg:reg): #lê registrador, função fundamental
        #modbus function 3 = read n registers
        return self.km3p.read_register(reg.address, reg.dec_point, 3, reg.singed)
    
    def get_power(self):
        return self.read(self.potency)
    
    def tune(self): #inicia/finaliza auto-tuning
        c = self.read(self.tune_onoff)
        if(c == 0):
            self.tune_onoff.value = 1
            self.write(self.tune_onoff)
        else:
            self.tune_onoff.value = 0
            self.write(self.tune_onoff)

    def get_pid_params(self): #lê valores do pid
        p = self.read(self.proportional)
        i = self.read(self.integral)
        d = self.read(self.derivative)
        return [p, i, d]
    
    def get_baud(self):#lê valores do baudrate
        c = self.read(self.baud)
        match c:
            case 0:
                baud = 1200
            case 1:
                baud = 2400
            case 2:
                baud = 9600
            case 3:
                baud = 19200
            case 4:
                baud = 38400
            case _:
                baud = 9600
        return baud

    def set_alarm(self, set_point:int, faixa:int): #set alarm, (valor desejado, faixa +-) limite superior = valor + faixa, limite inferior = valor - faixa
        self.alarm_1_high.value = set_point + faixa
        self.alarm_1_low.value = set_point - faixa
        self.alarm_1_low.singed = True if self.alarm_1_low.value < 0 else False
        self.alarm_1_high.singed = True if self.alarm_1_high.value < 0 else False
        self.write(self.alarm_1_type)
        self.write(self.alarm_1_func)
        self.write(self.alarm_1_high)
        self.write(self.alarm_1_low)
        self.write(self.out_3_func)
        self.write(self.out_3_alarm)

    def set_temperature(self, value=0): #seleciona o setpoint
        self.set_point1.value = value * (10**self.dec)
        self.write(self.set_point1)

    def temperature(self): #lê a temperatura
        t = self.read(self.measure_value)
        return t / (10**self.dec)
        


    def wait_temperature(self): #retorna true se o valor medido é o mesmo do setpoint, falso caso o contrário
        if(self.read(self.measure_value) != self.set_point1.value):
            return False
        return True

    def reset(self): #reseta todos os valores para padrão de fabrica
        self.write(self.reset_default)


