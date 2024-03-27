close all
% 
% a = readtable("EIS.csv")
% figure
% plot3(a.Real_m__,a.Imaginary,a.Frequency_Hz_)

b = readtable("SingleFreq5e-1.csv")
R = b.Real(b.Imaginary>0 & b.Imaginary<5);
I = b.Imaginary(b.Imaginary>0&b.Imaginary<5);
plot(R,I,mean(R),mean(I),'o')
[mean(R),mean(I)]

% b = readtable("DCL.csv")
% figure
% plot(b.Voltage)
% 
% figure
% plot(b.Current)