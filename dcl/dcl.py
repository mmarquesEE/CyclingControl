import pyvisa

class DCL:
    def __init__(self,serial_number="USB0::0x2A8D::0x3902::MY61001566::INSTR") -> None:
        self.rm = pyvisa.ResourceManager()
        self.inst = self.rm.open_resource(serial_number)
        print(self.inst.query("*IDN?"))

    def run(self,mode,values,filename='log1.csv',channels='1',time=[0.01],repetitions=1):
        self.inst.write(f"FUNC {mode}, (@{channels})")

        self.inst.write(f"{mode} 0.012, (@{channels})")
        
        self.inst.write(f"LIST:{mode} {''.join([str(e) + ',' for e in values])} (@{channels})")

        npad = len(values) - len(time)
        time_list = time.copy()
        time_list.extend(npad*[time[-1]])

        self.inst.write(
            f"LIST:DWEL {''.join([str(e) + ',' for e in time_list])} (@{channels})")
        self.inst.write(f"LIST:COUNT {repetitions}, (@{channels})")
        self.inst.write(f"LIST:TERM:LAST 0, (@{channels})")
        self.inst.write(f"LIST:STEP AUTO, (@{channels})")
        self.inst.write(f"{mode}:MODE LIST, (@{channels})")
        
        # self.inst.write("TRIG:SOURCE BUS")
        # self.inst.write(f"INIT (@{channels})")
        
        self.inst.write(f"SENS:DLOG:FUNC:VOLT 1, (@{channels})")
        self.inst.write(f"SENS:DLOG:FUNC:CURR 1, (@{channels})")
    
        # self.inst.write(f"SENS:DLOG:TIME {sum(time_list)}")
        # self.inst.write(f"SENS:DLOG:PER {min(time_list)}")
        
        # self.inst.write("TRIG:DLOG:SOUR BUS")
        # self.inst.write('INIT:DLOG \"External:\\' + filename + '\"')
        
        # self.inst.write(f"INP ON, (@{channels})")
        # self.inst.write(f"*TRG")