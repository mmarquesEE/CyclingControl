def funcDelog(v):
    try:
        # Habilitar a função de registro de dados de corrente
        v.write('SENS:DLOG:FUNC:CURR ON, (@1)')

        # Habilitar a função de registro de dados de tensão
        v.write('SENS:DLOG:FUNC:VOLT ON, (@1)')  

        # Definir o número de pontos na varredura
        v.write('SENS:SWE:POIN 2048, (@1)')  

        # Definir o intervalo de tempo entre as amostras
        v.write('SENS:SWE:TINT 0.001, (@1)') 

        # Iniciar a varredura
        v.write('SENS:SWE:STAR')

        # Procurar funcao que verifica se a medição esta completa

        # Ler os dados de corrente e tensão após a varredura
        corrente = v.query('SENS:DLOG:FUNC:CURR (@1)')  # Lê o status da função de corrente para o canal 1
        tensao = v.query('SENS:DLOG:FUNC:VOLT? (@1)')  # Lê o status da função de tensão para o canal 1

        print("Status da função de corrente:", corrente)
        print("Status da função de tensão:", tensao)

    finally:
        v.close()


