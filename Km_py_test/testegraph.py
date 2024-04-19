import Km3P_control as km
import time
import matplotlib.pyplot as plot

instrumento = km.km3(serial_port='COM8', decimal=1)

plot.ion()

temp = instrumento.temperature()
pot = instrumento.get_power()
sp = 0
instrumento.set_temperature(sp)
y_temp = [temp]
x_time = [0]
y_pot = [pot]
y_set = [sp]


temperatura = plot.plot(x_time, y_temp, label='temperatura')[0]
potencia = plot.plot(x_time, y_pot, label='potencia')[0]
setpoint = plot.plot(y_set, x_time, label='SetPoint')[0]
plot.ylim(max(y_temp)+1)
plot.pause(1)

plot.show()
i = 0
while True:
    i += 1
    y_temp.append(instrumento.temperature())
    y_pot.append(instrumento.get_power())
    y_set.append(sp)
    x_time.append(i)
    temperatura.remove()
    temperatura = plot.plot(x_time, y_temp, label='temperatura')[0]
    potencia = plot.plot(x_time, y_pot, label='potencia')[0]
    setpoint = plot.plot(y_set, x_time, label='SetPoint')[0]
    plot.ylim(max(y_temp))
    plot.xlim(i+5)
    time.sleep(1)