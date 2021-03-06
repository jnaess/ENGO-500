clc
clear
format longG


ppp = readmatrix("ppp_final.csv");
psr = readmatrix("psr_final.csv");
rtk = readmatrix("rtk_final.csv");

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

trueMeanLat = mean(rtk(:,23));
trueMeanLon = mean(rtk(:,24));
trueMeanH = mean(rtk(:,6));
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
for i = 1:size(psr,1)
   DiffPSR(i,1) = psr(i,23)-trueMeanLat; %Lat
   DiffPSR(i,2) = psr(i,24)-trueMeanLon; %Long
end

%RTK
DiffRTK = zeros(size(ppp,1),2);
for i = 1:size(rtk,1)
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
xlabel('Easting (m)');
ylabel('Northing (m)');
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
xlabel('Easting (m)');
ylabel('Northing (m)');
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
xlabel('Easting (m)');
ylabel('Northing (m)');
legend('Observed Coordinates','True Coordinates','Location','Best');
hold off


%Diff averaging and plotting (15 min intervals)
x = 1:97;
%PPP
PPP15minNorth = zeros(97,1);
PPP15minEast = zeros(97,1);
PosPPP = 0; %Position of row counter, does not change
for i = 1:96
    SumNorth = 0;
    SumEast = 0;
   for j = 1:900
       PosPPP = PosPPP + 1;
       SumNorth = SumNorth + DiffPPP(PosPPP,1);
       SumEast = SumEast + DiffPPP(PosPPP,2);
   end
    PPP15minNorth(i,1) = SumNorth/900;
    PPP15minEast(i,1) = SumEast/900;
end
%Stragglers
SumNorth = 0;
SumEast = 0;
LastVals = size(DiffPPP,1) - 96*900;
for j = 1:LastVals
    PosPPP = PosPPP + 1;
    SumNorth = SumNorth + DiffPPP(PosPPP,1);
    SumEast = SumEast + DiffPPP(PosPPP,2);
end
PPP15minNorth(97,1) = SumNorth/LastVals;
PPP15minEast(97,1) = SumEast/LastVals;
PPPAcrossRangeN = max(PPP15minNorth) - min(PPP15minNorth);
PPPAcrossRangeE = max(PPP15minEast) - min(PPP15minEast);
PPPAcrossSTDN = std(PPP15minNorth);
PPPAcrossSTDE = std(PPP15minEast);
PPPAcrossErrN = mean(PPP15minNorth);
PPPAcrossErrE = mean(PPP15minEast);
PPPAcrossVarN = PPPAcrossSTDN^2;
PPPAcrossVarE = PPPAcrossSTDE^2;

%PSR
PSR15minNorth = zeros(97,1);
PSR15minEast = zeros(97,1);
PosPSR = 0; %Position of row counter, does not change
for i = 1:96
    SumNorth = 0;
    SumEast = 0;
   for j = 1:900
       PosPSR = PosPSR + 1;
       SumNorth = SumNorth + DiffPSR(PosPSR,1);
       SumEast = SumEast + DiffPSR(PosPSR,2);
   end
    PSR15minNorth(i,1) = SumNorth/900;
    PSR15minEast(i,1) = SumEast/900;
end
%Stragglers
SumNorth = 0;
SumEast = 0;
LastVals = size(DiffPSR,1) - 96*900;
for j = 1:LastVals
    PosPSR = PosPSR + 1;
    SumNorth = SumNorth + DiffPSR(PosPSR,1);
    SumEast = SumEast + DiffPSR(PosPSR,2);
end
PSR15minNorth(97,1) = SumNorth/LastVals;
PSR15minEast(97,1) = SumEast/LastVals;
PSRAcrossRangeN = max(PSR15minNorth) - min(PSR15minNorth);
PSRAcrossRangeE = max(PSR15minEast) - min(PSR15minEast);
PSRAcrossSTDN = std(PSR15minNorth);
PSRAcrossSTDE = std(PSR15minEast);
PSRAcrossErrN = mean(PSR15minNorth);
PSRAcrossErrE = mean(PSR15minEast);
PSRAcrossVarN = PSRAcrossSTDN^2;
PSRAcrossVarE = PSRAcrossSTDE^2;

%RTK
RTK15minNorth = zeros(97,1);
RTK15minEast = zeros(97,1);
PosRTK = 0; %Position of row counter, does not change
for i = 1:96
    SumNorth = 0;
    SumEast = 0;
   for j = 1:900
       PosRTK = PosRTK + 1;
       SumNorth = SumNorth + DiffRTK(PosRTK,1);
       SumEast = SumEast + DiffRTK(PosRTK,2);
   end
    RTK15minNorth(i,1) = SumNorth/900;
    RTK15minEast(i,1) = SumEast/900;
end
%Stragglers
SumNorth = 0;
SumEast = 0;
LastVals = size(DiffRTK,1) - 96*900;
for j = 1:LastVals
    PosRTK = PosRTK + 1;
    SumNorth = SumNorth + DiffRTK(PosRTK,1);
    SumEast = SumEast + DiffRTK(PosRTK,2);
end
RTK15minNorth(97,1) = SumNorth/LastVals;
RTK15minEast(97,1) = SumEast/LastVals;
RTKAcrossRangeN = max(RTK15minNorth) - min(RTK15minNorth);
RTKAcrossRangeE = max(RTK15minEast) - min(RTK15minEast);
RTKAcrossSTDN = std(RTK15minNorth);
RTKAcrossSTDE = std(RTK15minEast);
RTKAcrossErrN = mean(RTK15minNorth);
RTKAcrossErrE = mean(RTK15minEast);
RTKAcrossVarN = RTKAcrossSTDN^2;
RTKAcrossVarE = RTKAcrossSTDE^2;
%Plot Intervals
figure
hold on
plot(x,PSR15minNorth(:,1),'g')
plot(x,PPP15minNorth(:,1),'b')
plot(x,RTK15minNorth(:,1),'r')
legend('PSR','PPP','RTK')
title('Northing Across Track Accuracy over time')
ylabel('Pass to Pass Accuracy (m)')
xlabel('15 minute intervals')
hold off
figure
hold on
plot(x,PSR15minEast(:,1),'g')
plot(x,PPP15minEast(:,1),'b')
plot(x,RTK15minEast(:,1),'r')
legend('PSR','PPP','RTK')
title('Easting Across Track Accuracy over time')
ylabel('Pass to Pass Accuracy (m)')
xlabel('15 minute intervals')
hold off

%Position Jumps
rtkJump = readmatrix('rtk_jump3.csv');
psrJump = readmatrix('psr_jump.csv');
pppJump = readmatrix('ppp_jump.csv');
checkJumps = zeros(1,3); %Holds number of jumps, RTK, PSR, PPP
%Check number of Jumps
for i = 1:size(rtkJump,1)
   if rtkJump(i,2) == 1
      checkJumps(1,1) = checkJumps(1,1)+1; 
   end
end
for i = 1:size(psrJump,1)
   if psrJump(i,2) == 1
      checkJumps(1,2) = checkJumps(1,2)+1; 
   end
end
for i = 1:size(pppJump,1)
   if pppJump(i,2) == 1
      checkJumps(1,3) = checkJumps(1,3)+1; 
   end
end
counter = 1;
indexJumpRTK = zeros(checkJumps(1,1),24);
indexJumpPSR = zeros(checkJumps(1,2),24);
indexJumpPPP = zeros(checkJumps(1,3),24);
for i = 1:size(rtkJump,1)
   if rtkJump(i,2) == 1
      indexJumpRTK(counter,:) = rtk(i,:);
      counter = counter+1;
   end
end
counter = 1;
for i = 1:(size(psrJump,1)/2)
   if psrJump(i,2) == 1
      indexJumpPSR(counter,:) = psr(i,:);
   end
end
counter = 1;
for i = 1:(size(pppJump,1))
   if pppJump(i,2) == 1
      indexJumpPPP(counter,:) = ppp(i,:);
   end
end



figure
%RTK Jumps
hold on
sz = 25;
c = linspace(1,10,length(rtk(:,24)));
scatter(rtk(:,24),rtk(:,23),sz,c,'filled')
scatter(indexJumpRTK(:,24),indexJumpRTK(:,23),sz,'d','MarkerFaceColor',[1 .1 .1])
colorbar('southoutside','Ticks',[1,3,5,7,10],...
         'TickLabels',{'Starting Epoch','','','','Final Epoch'})

title('RTK measurements with Jumps')
xlabel('Easting');
ylabel('Northing');
legend('Observed Coordinates','Coordinates Jumps','Location','Best');
hold off

figure
%PSR Jumps
hold on
sz = 25;
c = linspace(1,10,length(psr(:,24)));
scatter(psr(:,24),psr(:,23),sz,c,'filled')
scatter(indexJumpPSR(:,24),indexJumpPSR(:,23),sz,'d','MarkerFaceColor',[1 .1 .1])
colorbar('southoutside','Ticks',[1,3,5,7,10],...
         'TickLabels',{'Starting Epoch','','','','Final Epoch'})

title('PSR measurements with Jumps')
xlabel('Easting');
ylabel('Northing');
legend('Observed Coordinates','Coordinates Jumps','Location','Best');
hold off

figure
%PPP Jumps
hold on
sz = 25;
c = linspace(1,10,length(ppp(:,24)));
scatter(ppp(:,24),ppp(:,23),sz,c,'filled')
scatter(indexJumpPPP(:,24),indexJumpPPP(:,23),sz,'d','MarkerFaceColor',[1 .1 .1])
colorbar('southoutside','Ticks',[1,3,5,7,10],...
         'TickLabels',{'Starting Epoch','','','','Final Epoch'})

title('PPP measurements with Jumps')
xlabel('Easting');
ylabel('Northing');
legend('Observed Coordinates','Coordinates Jumps','Location','Best');
hold off