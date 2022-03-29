clc
clear
format longG

%Inputs still required
ppp = readmatrix("ppp.csv");
psr = readmatrix("psr.csv");
rtk = readmatrix("rtk.csv");

%lat 23,long 24,height 6,sigmalat 9,sigmalong 10,sigmaheight 11

rtklatAve = mean(rtk(:,23));
rtklatStd = std(rtk(:,23));
rtklatErrorAve = mean(rtk(:,9));
rtklatErrorVar = std(rtk(:,9));
rtklonAve = mean(rtk(:,24));
rtklonStd = std(rtk(:,24));
rtklonErrorAve = mean(rtk(:,10));
rtklonErrorVar = std(rtk(:,10));
rtkhieghtAve = mean(rtk(:,6));
rtkheightStd = std(rtk(:,6));
rtkhieghtErrorAve = mean(rtk(:,11));
rtkheightErrorVar = std(rtk(:,11));



