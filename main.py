from eis.eis import EIS
from dcl.dcl import DCL
import pandas as pd

if __name__ == "__main__":
    eis = EIS()
    eis.run("EIS.csv")

    dcl = DCL()
    dcl.reset()
    df = dcl.run('CURR',[0.6,0.5,0.22,0.5,0.1],list_time=[1.5,1])

    print(df.head())
    