from eis.eis import EIS
from dcl.dcl import DCL
import pandas as pd

if __name__ == "__main__":
    eis = EIS()

    # Warbug Impedance
    eis.start_frequency = "0.1"
    eis.stop_frequency = "0.5"
    eis.points = "5"
    eis.logarithmic = "0"
    eis.reset()
    df_Warbug1 = eis.run()
    print("OK")
    eis.start_frequency = "0.5"
    eis.stop_frequency = "1.0"
    eis.points = "5"
    eis.reset()
    df_Warbug2 = eis.run()
    print("OK")

    # Double Layer Capacitance and Charge Transfer Resistance
    eis.start_frequency = "1.0"
    eis.stop_frequency = "100"
    eis.points = "20"
    eis.logarithmic = "1"
    eis.reset()
    df_DLC_CTR1 = eis.run()
    print("OK")
    eis.start_frequency = "100.0"
    eis.stop_frequency = "2000"
    eis.points = "-1"
    eis.reset()
    df_DLC_CTR2 = eis.run()
    print("OK")

    df = pd.concat([df_Warbug1,df_Warbug2,df_DLC_CTR1,df_DLC_CTR2],ignore_index=True)

    # dcl = DCL()
    # dcl.reset()
    # df = dcl.run('CURR',[0.6,0.5,0.22,0.5,0.1],list_time=[1.5,1])

    df.to_csv("EIS.csv")
    print(df)
    