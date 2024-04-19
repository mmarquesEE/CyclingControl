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

    def run(self, mode, list_values, eost_values, channels='1',
        list_time=[0.01], repetitions=1, sample_time=0.01, filename="DCL.csv"):
        
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
        
        self.inst.write(f"SENS:DLOG:FUNC:VOLT 1, (@1,2)")
        self.inst.write(f"SENS:DLOG:FUNC:CURR 1, (@1,2)")
        
        self.inst.write(f"SENS:DLOG:TIME {sum(time_list)}")
        self.inst.write(f"SENS:DLOG:PER {sample_time}")
        
        self.inst.write(f"DIG:PIN1:FUNC TOUT")
        self.inst.write(f"DIG:PIN1:POL NEG")

        self.inst.write("TRIG:TRAN:SOUR BUS")
        self.inst.write("TRIG:DLOG:SOUR BUS")

        self.inst.write(f"INIT:TRAN (@{channels})")
        self.inst.write(f'INIT:DLOG "Internal:/log1.dlog"')
        
        self.inst.write(f"INP ON, (@{channels})")
        self.inst.write("*TRG")
        
        time.sleep(sum(time_list) + 5)

        fetch_points = int(sum(time_list) / sample_time)
        dfi = []
        for i in range(fetch_points):
            dout = self.inst.query(f"FETC:DLOG? 1, (@{channels})")
            dout_float = [float(a) for a in dout.split(",")]
            dfi.append(
                pd.DataFrame(data={"Voltage": dout_float[0], "Current": dout_float[1]}, index=[0]))
        
        df = pd.concat(dfi, ignore_index=True)
        df.to_csv(filename)
        
        return df

    



