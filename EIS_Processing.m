close all

a = readtable("EIS.csv")
figure
plot(a.Real_m__,a.Imaginary,'o')

b = readtable("DCL.csv")
figure
plot(b.Voltage)

figure
plot(b.Current)