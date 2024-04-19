from bokeh.plotting import figure, show
from time import sleep
import Km3P_control as km

km3p = km.km3(serial_port="COM8", decimal=1)

values = [[],
          [],
          []]
pid = km3p.get_pid_params()
pid_init = km3p.get_pid_params()
x = []
sp = 50
km3p.set_temperature(sp)

graph = figure(title="Temperature Control", x_axis_label="segundos", y_axis_label="y")
graph.line(x, values[0], legend_label="Temp.", line_color="blue", line_width=1)
graph.line(x, values[1], legend_label="Pot. %", line_color="red", line_width=1)
graph.line(x, values[2], legend_label="SetPoint", line_color="green", line_width=1)

def update_values(setpoint:int = 0):
    global pid, values, sp, km3p

    if(setpoint != sp):
        km3p.set_temperature(setpoint)
        sp = setpoint

    values[0].append(km3p.temperature())
    values[1].append(km3p.get_power())
    values[2].append(setpoint)
    pid = km3p.get_pid_params()


for i in range(60):
    x.append(i)
    update_values(sp)
    print(f"{x[i]} segundos ja se passaram")
    sleep(1)

km3p.set_temperature(0)
show(graph)