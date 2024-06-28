a = readtable('First_Test.csv');

figure
yyaxis left;
plot(a.Current1), yyaxis right, plot(a.Voltage1);