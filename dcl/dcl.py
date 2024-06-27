import pyvisa
import time
import pandas as pd


class DCL:
    def __init__(self,serial_number="USB0::0x2A8D::0x3902::MY61001566::INSTR") -> None:
        self.rm = pyvisa.ResourceManager()
        self.inst = self.rm.open_resource(serial_number)
        print(self.inst.query("*IDN?"))

    def reset(self):
        while int(self.inst.query("*RST;*OPC?")) != 1:
            pass
        
        self.inst.write("SENS:DLOG:FUNC:VOLT 0, (@1,2)")
        self.inst.write("SENS:DLOG:FUNC:CURR 0, (@1,2)")

    def run(self, mode, list_values, channels, cutof_voltage,
        list_time=[0.01], repetitions=1, sample_time=0.01, filename=None):
        
        self.reset()

        self.inst.write(f"VOLT:INH:VON {cutof_voltage}, (@{channels})")
        self.inst.write(f"VOLT:INH:VON:MODE LIVE, (@{channels})")

        self.inst.write(f"FUNC {mode}, (@{channels})")
        self.inst.write(f"{mode} 0.012, (@{channels})")
        self.inst.write(f"LIST:{mode} {''.join([str(e) + ',' for e in list_values])} (@{channels})")

        npad = len(list_values) - len(list_time)
        time_list = list_time.copy()
        time_list.extend(npad * [list_time[-1]])

        nlist = len(list_values)
        eost_values = [0] * (nlist - 1) + [1]

        self.inst.write(f"LIST:DWEL {''.join([str(e) + ',' for e in time_list])} (@{channels})")
        self.inst.write(f"LIST:COUNT {repetitions}, (@{channels})")
        self.inst.write(f"LIST:TERM:LAST 0, (@{channels})")
        self.inst.write(f"LIST:STEP AUTO, (@{channels})")
        self.inst.write(f"{mode}:MODE LIST, (@{channels})")
        self.inst.write(f"LIST:TOUT:EOST {','.join([str(e) for e in eost_values])}, (@{channels})")
        
        self.inst.write(f"DIG:PIN1:FUNC TOUT")
        self.inst.write(f"DIG:PIN1:POL NEG")

        self.inst.write("TRIG:TRAN:SOUR BUS")
        self.inst.write(f"INIT:TRAN (@{channels})")

        self.inst.write(f"INP ON, (@{channels})")
        
        self.inst.write(f"SENS:FUNC:CURR 1, (@{channels})")
        self.inst.write(f"SENS:FUNC:VOLT 1, (@{channels})")

        ch_n = len(channels.split(sep=","))
        self.inst.write(f"SENS:SWE:POIN {2*ch_n*int(sum(list_time)/sample_time)}, (@{channels})")
        self.inst.write(f"SENS:SWE:TINT {sample_time}, (@{channels})")

        self.inst.write("*TRG")
        
        while all(map(lambda x: x > 0.02, [
            float(a) for a in self.inst.query(f"MEAS:CURR? (@{channels})").split(sep=",")
        ])):
            pass
            
        self.inst.write("*RST")

        data = []
        for ch in [int(c) for c in channels.split(sep=",")]:
            curr = [float(a) for a in self.inst.query(f"MEAS:ARR:CURR? (@{channels})").split(sep=",")]
            volt = [float(a) for a in self.inst.query(f"MEAS:ARR:VOLT? (@{channels})").split(sep=",")]

            row = dict()
            for i in range(0,len(curr)):
                row[f"Voltage{ch}"] = volt[i]
                row[f"Current{ch}"] = curr[i]
                data.append(row)
        df = pd.DataFrame(data)
        
        if filename:
            df.to_csv(filename)
        
        return df

    



