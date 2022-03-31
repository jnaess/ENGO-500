clc
clear
format longG

%Inputs still required
ppp = readmatrix("ppp.csv");
psr = readmatrix("psr.csv");
rtk = readmatrix("rtk.csv");
rtktable = readtable("rtk.csv");
%lat 23,long 24,height 6,sigmalat 9,sigmalong 10,sigmaheight 11

rtklat = rtk(:,23);
rtklon = rtk(:,24);

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

trueMeanLat = mean(psr(:,23));
trueMeanLon = mean(psr(:,24));
trueMeanH = mean(psr(:,6));
%Jump Detection

%RTK
% JumpRTK = zeros(size(rtk,1),24);
% for i = 1:size(rtk,1)
%     if rtklat(i,1)>(rtklatAve+rtklatErrorAve*3)| rtklat(i,1)<(rtklatAve-rtklatErrorAve*3)|rtklon(i,1)>(rtklonAve+rtklonErrorAve*3)| rtklon(i,1)<(rtklonAve-rtklonErrorAve*1)
%         JumpRTK(i,:) = rtk(i,:);
%     end 
% end
% JumpRTK( all(~JumpRTK,2), : ) = [];


%Diff: Lat, Long
%PPP
DiffPPP = zeros(size(ppp,1),2);
for i = 1:size(ppp,1)
   DiffPPP(i,1) = ppp(i,23)-trueMeanLat; %Lat
   DiffPPP(i,2) = ppp(i,24)-trueMeanLon; %Long
end

%PSR
DiffPSR = zeros(size(ppp,1),2);
for i = 1:size(ppp,1)
   DiffPSR(i,1) = psr(i,23)-trueMeanLat; %Lat
   DiffPSR(i,2) = psr(i,24)-trueMeanLon; %Long
end

%RTK
DiffRTK = zeros(size(ppp,1),2);
for i = 1:size(ppp,1)
   DiffRTK(i,1) = rtk(i,23)-trueMeanLat; %Lat
   DiffRTK(i,2) = rtk(i,24)-trueMeanLon; %Long
end

StddiffPPPlat = std(DiffPPP(:,1));
StddiffPPPlon = std(DiffPPP(:,2));
StddiffPSRlat = std(DiffPSR(:,1));
StddiffPSRlon = std(DiffPSR(:,2));
StddiffRTKlat = std(DiffRTK(:,1));
StddiffRTKlon = std(DiffRTK(:,2));

figure
%RTK
hold on
sz = 25;
c = linspace(1,10,length(rtk(:,24)));
scatter(rtk(:,24),rtk(:,23),sz,c,'filled')
scatter(trueMeanLon,trueMeanLat,sz,'d','MarkerFaceColor',[1 .1 .1])
colorbar('southoutside','Ticks',[1,3,5,7,10],...
         'TickLabels',{'Starting Epoch','','','','Final Epoch'})

title('RTK measurements vs True Value')
xlabel('Easting');
ylabel('Northing');
legend('Observed Coordinates','True Coordinates','Location','Best');
hold off

figure
%PSR
hold on
sz = 25;
c = linspace(1,10,length(psr(:,24)));
scatter(psr(:,24),psr(:,23),sz,c,'filled')
scatter(trueMeanLon,trueMeanLat,sz,'d','MarkerFaceColor',[1 .1 .1])
colorbar('southoutside','Ticks',[1,3,5,7,10],...
         'TickLabels',{'Starting Epoch','','','','Final Epoch'})

title('PSR measurements vs True Value')
xlabel('Easting');
ylabel('Northing');
legend('Observed Coordinates','True Coordinates','Location','Best');
hold off

figure
%PPP
hold on
sz = 25;
c = linspace(1,10,length(ppp(:,24)));
scatter(ppp(:,24),ppp(:,23),sz,c,'filled')
scatter(trueMeanLon,trueMeanLat,sz,'d','MarkerFaceColor',[1 .1 .1])
colorbar('southoutside','Ticks',[1,3,5,7,10],...
         'TickLabels',{'Starting Epoch','','','','Final Epoch'})

title('PPP measurements vs True Value')
xlabel('Easting');
ylabel('Northing');
legend('Observed Coordinates','True Coordinates','Location','Best');
hold off


