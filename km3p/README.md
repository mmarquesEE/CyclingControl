### Todo:
- [x] Terminar um código usável
- [ ] Renomear o código para utilizalo como uma biblioteca
- [ ] Transforma-lo e testa-lo como uma biblioteca
      
## Funções
### Para mais informações, consultar o [manual](https://github.com/mmarquesEE/CyclingControl/blob/Lucas-Branch/km3p/ISTR_P_K-1-3series_E_03_--.pdf) 
- self.write(register:class) = escreve em um registrador, recebe um objeto registrador (precisa ser pelo menos writable)
- self.read(register:class) = retorna um valor em um registrador (precisa ser pelo menos readable)
- self.get_baud() = retorna o baud_rate configurado no controlador
- self.set_alarm(temperatura, faixa_de_erro) = configura o controlador para fechar a porta OUT3 dentro de uma temperatura
- self.set_temperature(temperatura) = seleciona a temperatura desejada ao qual o controlador almejará alcançar
- self.temperature()->int = retorna a temperatura atual do sensor
- self.wait_temperature()->bool = retorna falso se a temperatura não é a desejada, e true se a temperatura é a desejada
- self.reset() = reseta as configurações para as de fabrica
  
## Known issues:
- dependendo do registrador, o controlador(KM3P) demora a retornar os bits de confirmação, quebrando o codigo com um NoResponseError
- durante o reset das configurações, o controlador(KM3P) perde comunicação com a porta serial, quebrando o código com um NoResponseError
- self.set_alarm(temp, faixa) não esta aceitando faixa de erro > 0
