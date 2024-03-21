close all

a = readtable("EIS.csv")
plot(a.Real_m__,a.Imaginary,'o')