import serial
import time


class MCU:
    def __init__(self,com_port="COM3",baud=9600):
        self.serial = serial.Serial(com_port,baud)
    
    def query_alarm(self,equip):
        self.serial.write(f',{equip}_ALARM?,'.encode())
        resposta = self.serial.readline().decode().strip()

        if resposta == f"{equip}_ALARM ON":
            return True
        elif resposta == f"{equip}_ALARM OFF":
            return False
        else:
            return None
        
    def reset_eis(self,eis_ch):
        self.serial.write(f',RESET_EIS{eis_ch},'.encode())

    def cycler(self,onoff):
        self.serial.write(f',CHARGE {"ON" if onoff else "OFF"},'.encode())
    
    def dcl_eis(self,onoff):
        self.serial.write(f',DCL_EIS {"ON" if onoff else "OFF"},'.encode())


try:
    # Inicializa a conexão serial
    conexao_serial = serial.Serial("COM3", 9600)
    
    # Verifica se a porta foi aberta corretamente
    if conexao_serial.isOpen():
        print("Conexão serial estabelecida com sucesso!")

        time.sleep(2)
        # Envia um comando
        comando = ",CHARGE ON,"  # Substitua pelo comando desejado
        conexao_serial.write(comando.encode())

        time.sleep(2)
        
        comando = ",CHARGE OFF,"  # Substitua pelo comando desejado
        conexao_serial.write(comando.encode())

        time.sleep(2)
        
        comando = ",DCL_EIS ON,"  # Substitua pelo comando desejado
        conexao_serial.write(comando.encode())

        time.sleep(2)
        
        comando = ",DCL_EIS OFF,"  # Substitua pelo comando desejado
        conexao_serial.write(comando.encode())
        
        time.sleep(2)
        
        comando = ",TC_ALARM?,"  # Substitua pelo comando desejado
        conexao_serial.write(comando.encode())

        # Aguarda a resposta do microcontrolador, se necessário
        resposta = conexao_serial.readline().decode().strip()
        print("Resposta do microcontrolador:", resposta)

        # Aguarda um pouco antes de fechar a porta
        time.sleep(2)

        comando = ",DCL_ALARM?,"  # Substitua pelo comando desejado
        conexao_serial.write(comando.encode())

        # Aguarda a resposta do microcontrolador, se necessário
        resposta = conexao_serial.readline().decode().strip()
        print("Resposta do microcontrolador:", resposta)

        # Aguarda um pouco antes de fechar a porta
        time.sleep(2)

    else:
        print("Não foi possível abrir a porta serial.")
finally:
    # Fecha a conexão serial
    conexao_serial.close()
    print("Conexão serial fechada.")
