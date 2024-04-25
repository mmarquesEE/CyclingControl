from dcl.dcl import DCL

def main():

    dcl_instance = DCL()
    
    mode = "CURR"  
    list_values = [1, 2, 3]  
    channels = '1' 
    list_time = [0.01, 0.02, 0.03]  
    repetitions = 1 
    sample_time = 0.01 
    filename = "DCL_data.csv" 

    # Chamando o método run
    df_result = dcl_instance.run(mode, list_values, channels=channels,
                                 list_time=list_time, repetitions=repetitions,
                                 sample_time=sample_time, filename=filename)

    print(df_result.head()) 

if __name__ == "__main__":
    main()