import Km3P_control as km3p

km = km3p.km3(serial_port='COM8')
km.set_alarm(23, 1)