from dcl.dcl import DCL
from mcu.mcu import MCU
from time import sleep

def main():
    mcu_instance = MCU()

    sleep(1)
    mcu_instance.dcl_eis(True)
    sleep(1)
    mcu_instance.dcl_eis(False)

    dcl_instance = DCL()
    mode = "CURR" 
    channels = '1'
    curr_value = 1.3
    cutoff_voltage = 10

    df_result = dcl_instance(mode, channels, curr_value, cutoff_voltage)
    
    # dcl_instance = DCL()
    
    # mode = "CURR"  
    # list_values = [1, 2, 3]  
    # channels = '1'
    # cutoff_voltage = 10
    # list_time = [1, 1, 1]  
    # repetitions = 1 
    # sample_time = 0.01 
    # filename = "DCL_data.csv" 

    # # Chamando o método run
    # df_result = dcl_instance.run(mode, list_values, channels, cutoff_voltage,
    #                              list_time=list_time, repetitions=repetitions,
    #                              sample_time=sample_time, filename=filename)

    # print(df_result.head()) 

if __name__ == "__main__":
    main()