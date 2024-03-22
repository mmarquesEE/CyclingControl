import numpy as np
import pandas as pd
import serial.tools
import clr
import sys

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

class NoConnectionException(Exception):
    """The device is not connected! Verify the COM port"""

class EIS:
    def __init__(
            self,
            com_port="COM8",
            sensorpal_installation="C:\\Program Files (x86)\\Analog Devices\\SensorPal",
            start_frequency="100",
            stop_frequency="1000",
            points="-1",
            dc_bias="1200",
            ac_amplitude="300",
            logarithmic="1",
            calibration_resistor="50"
        ) -> None:
        
        self.com_port = com_port
        self.sensorpal_installation = sensorpal_installation
        self.start_frequency = start_frequency
        self.stop_frequency = stop_frequency
        self.points=points
        self.dc_bias=dc_bias
        self.ac_amplitude=ac_amplitude
        self.logarithmic=logarithmic
        self.calibration_resistor=calibration_resistor

        sys.path.append('%s' % self.sensorpal_installation)

        clr.AddReference('SensorPal.API')
        from SensorPal.API import API as SensorPalAPI

        self.sensorpal = SensorPalAPI()

        try:
            self.sensorpal.OpenConnection(com_port)
        except Exception as e:
            print(e)
            print("I was unable to open '%s'. Is it connected?" % com_port)
        else:
            self.technique = "Battery Impedance"
            self.technique_parameters = self.sensorpal.GetDefaultTechniqueParameters(self.technique)

            self.sensorpal.UpdateTechniqueParameter(self.technique, self.technique_parameters,
                "Start Frequency", self.start_frequency)
            self.sensorpal.UpdateTechniqueParameter(self.technique, self.technique_parameters,
                "Stop Frequency", self.stop_frequency)
            self.sensorpal.UpdateTechniqueParameter(self.technique, self.technique_parameters,
                "Points", self.points)
            self.sensorpal.UpdateTechniqueParameter(self.technique, self.technique_parameters,
                "DC Bias", self.dc_bias)
            self.sensorpal.UpdateTechniqueParameter(self.technique, self.technique_parameters,
                "AC Amplitude", self.ac_amplitude)
            self.sensorpal.UpdateTechniqueParameter(self.technique, self.technique_parameters,
                "Logarithmic", self.logarithmic)
            self.sensorpal.UpdateTechniqueParameter(self.technique, self.technique_parameters,
                "Calibration Resistor", self.calibration_resistor)
            
            self.sensorpal.UpdateTechniqueParameter(self.technique, self.technique_parameters,
                "Enable", "1")
    
    def run(self, filename="EIS.csv"):
        try:
            self.sensorpal.Measure(self.technique, self.technique_parameters)
        except Exception as e:
            print(e)
            raise NoConnectionException
        else:
            dfi = []
            while self.sensorpal.IsMeasuring():
                graph_data = self.sensorpal.GetGraphData("Nyquist")
                if graph_data:
                    dfi.append(get_data_as_df(graph_data))
                    
            self.sensorpal.CloseConnection()
            df = pd.concat(dfi,ignore_index=True)
            df.to_csv(filename)

            return df
