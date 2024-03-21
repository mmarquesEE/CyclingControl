import numpy as np
import pandas as pd
import serial.tools
import clr
import sys

com_port = "COM8"
sensorpal_installation = "C:\\Program Files (x86)\\Analog Devices\\SensorPal"

sys.path.append('%s' % sensorpal_installation)

clr.AddReference('SensorPal.API')
from SensorPal.API import API as SensorPalAPI


def get_data_as_df(graph_data):
    dict_ = dict()
    for field_index in range(0, len(graph_data.InfoPaneNames)):
        if graph_data.InfoPaneNames[field_index]:
            try:
                value = float(graph_data.InfoPaneValues[field_index])
            except:
                value = graph_data.InfoPaneValues[field_index]

            dict_[graph_data.InfoPaneNames[field_index]] = value
    
    return pd.DataFrame(data=dict_,index=[0])


if __name__ == "__main__":

    sensorpal = SensorPalAPI()
    try:
        sensorpal.OpenConnection(com_port)
    except Exception as e:
        print(e)
        print("I was unable to open '%s'. Is it connected?" % com_port)
    else:

        technique = "Battery Impedance"
        technique_parameters = sensorpal.GetDefaultTechniqueParameters(technique)

        sensorpal.UpdateTechniqueParameter(technique, technique_parameters,
            "Start Frequency", "100")
        sensorpal.UpdateTechniqueParameter(technique, technique_parameters,
            "Stop Frequency", "1000")
        sensorpal.UpdateTechniqueParameter(technique, technique_parameters,
            "Enable", "1")

        sensorpal.Measure(technique, technique_parameters)

        dfi = []
        while sensorpal.IsMeasuring():
            graph_data = sensorpal.GetGraphData("Nyquist")
            if graph_data:
                dfi.append(get_data_as_df(graph_data))
                

        sensorpal.CloseConnection()
        df = pd.concat(dfi,ignore_index=True)
        print(df)
        df.to_csv("EIS.csv")
