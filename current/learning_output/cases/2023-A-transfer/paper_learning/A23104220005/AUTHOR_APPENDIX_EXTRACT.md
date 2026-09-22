# Converted appendix text; not an executable MATLAB bundle

## Page 38

```text
                                附录

%% 问题一
clear;
clc;
close all;

%% Model Parameters
SIFS = 16; slot_time = 9; DIFS = 43; %us
payload_bits = 12000; mac_header_bits = 240; %bits
physical_rate = 455.8; %Mbps
payload = payload_bits / physical_rate; mac_header = mac_header_bits
   /physical_rate; %us
phy_header = 13.6; ACK = 32; ACKTimeout = 65; %us
%packet = payload + mac_header;
CWmin = 16;
m = 6;   %maxStage
r = 32; %maxRetransCnt
sim_time = 0;
throughput = [];
throughput_ap1 = [];
throughput_ap2 = [];
collision_num = [];
collision_ratio = [];

%% Simulation
fprintf('Simulating...\n');
for sim_cnt = 1:300
ap_num = 2;
suc_pkt = 0;
suc_pkt_single = [0 0];
tran_time = 0;
collision_pkt = 0;
ap_stage = zeros(1,ap_num);
ap_retrans = zeros(1,ap_num);
next_tran_time = zeros(1,ap_num);

for i = 1:ap_num % 初始化随机退避时间
ap_stage(i) = 0;
next_tran_time(i) =floor(CWmin * rand) * slot_time;
end

while tran_time < 1000000
tran_time = min(next_tran_time);
no_tran = sum(tran_time == next_tran_time);

if no_tran == 1 % 传输成功
suc_pkt = suc_pkt + 1;
for i = 1:ap_num
if next_tran_time(i) == tran_time %筛选传输节点
suc_pkt_single(i) = suc_pkt_single(i) + 1;
ap_stage(i) = 0;
ap_retrans(i) = 0;


                                    37
```

[Visual fallback](page_images/page_038.jpg)

## Page 39

```text
next_tran_time(i) = next_tran_time(i) + phy_header + mac_header +
   payload + SIFS+ACK+DIFS+floor(CWmin*rand)*slot_time;
if tran_time >= 1000000
sim_time = next_tran_time (i) + phy_header + mac_header + payload +
   SIFS + ACK + DIFS;
end
else
next_tran_time(i) = next_tran_time(i) + phy_header + mac_header +
   payload + SIFS+ACK+DIFS;
end
end

else % 冲突
collision_pkt = collision_pkt + 1;
for i = 1:ap_num
if next_tran_time(i) == tran_time
if ap_stage(i) < m
ap_stage(i) = ap_stage(i) + 1;
end
if ap_retrans(i) < r
ap_retrans(i) = ap_retrans(i) + 1;
else
ap_stage(i) = 0;
ap_retrans(i) = 0;
end
next_tran_time(i)=next_tran_time(i) + phy_header + mac_header +
   payload + ACKTimeout + DIFS +
   floor(2^ap_stage(i)*CWmin*rand)*slot_time;
end
end
end
end
throughput = [throughput physical_rate * suc_pkt * payload /
   sim_time];
throughput_ap1 = [throughput_ap1 physical_rate * suc_pkt_single(1) *
   payload / sim_time];
throughput_ap2 = [throughput_ap2 physical_rate * suc_pkt_single(2) *
   payload / sim_time];
collision_num = [collision_num collision_pkt];
collision_ratio = [collision_ratio collision_pkt / (collision_pkt +
   suc_pkt)];
end

%% plot total throughput
plot(1:1:300,throughput,'LineWidth',1);
title('系统吞吐量','FontSize',15,'FontName','楷体')
xlabel('时间/s','FontSize',15,'FontName','楷体');
ylabel('吞吐量/Mbps','FontSize',15,'FontName','楷体');
saveas(gcf,
   ['C:\Users\A\Desktop\数学建模\problem1\totalThroughput.svg']);

%% plot single ap throughput
plot(1:1:300,throughput_ap1,1:1:300,throughput_ap2,'LineWidth',1);
title('单AP吞吐量','FontSize',15,'FontName','楷体')


                                  38
```

[Visual fallback](page_images/page_039.jpg)

## Page 40

```text
xlabel('时间/s','FontSize',15,'FontName','楷体');
ylabel('吞吐量/Mbps','FontSize',15,'FontName','楷体');
l = legend('AP1','AP2');
set(l,'FontSize',12);
saveas(gcf,
   ['C:\Users\A\Desktop\数学建模\problem1\singleThroughput.svg']);

%% plot number of collision
% yyaxis left;
%
   plot(1:1:300,collision_num,'LineWidth',1,'Color',[255/255,128/255,0/255]);
% title('碰撞数据包分析','FontSize',15,'FontName','楷体')
% xlabel('时间/s','FontSize',15,'FontName','楷体');
%
% yyaxis right;
%
   plot(1:1:300,collision_ratio,'LineWidth',1,'Color',[64/255,105/255,224/255]);
% ylim([0,0.1]);
% legend('碰撞数量','碰撞比例','FontName','楷体');
% saveas(gcf,
   ['C:\Users\A\Desktop\数学建模\problem1\collisionNum.svg']);
plot(1:1:300,collision_ratio,'LineWidth',1,'Color',[64/255,105/255,224/255])
title('碰撞数据包分析','FontSize',15,'FontName','楷体')
xlabel('时间/s','FontSize',15,'FontName','楷体');
ylabel('碰撞比例','FontSize',15,'FontName','楷体');
close all;

%% plot cdf of throughput
[h1, stats1] = cdfplot(throughput);
title('经验CDF','FontSize',15,'FontName','楷体');
xlabel('吞吐量/Mbps','FontSize',15,'FontName','楷体');
saveas(gcf, ['C:\Users\A\Desktop\数学建模\problem1\troughoutCDF.svg']);
[h2, stats2] = cdfplot(throughput_ap1);
[h3, stats3] = cdfplot(throughput_ap2);
[h4, stats4] = cdfplot(collision_ratio);


%% 问题二
clear;
clc;
close all;

%% Model Parameters
SIFS = 16; slot_time = 9; DIFS = 43; %us
payload_bits = 12000; mac_header_bits = 240; %bits
physical_rate = 275.3; %Mbps
payload = payload_bits / physical_rate; mac_header = mac_header_bits
   /physical_rate; %us
phy_header = 13.6; ACK = 32; ACKTimeout = 65; %us
%packet = payload + mac_header;
CWmin = 16;
m = 6;   %maxStage
r = 32; %maxRetransCnt
sim_time = 0;


                                  39
```

[Visual fallback](page_images/page_040.jpg)

## Page 41

```text
throughput = [];
throughput_ap1 = [];
throughput_ap2 = [];
same_num = [];
same_ratio = [];

%% Simulation
fprintf('Simulating...\n');
for sim_cnt = 1:300
ap_num = 2;
suc_pkt = 0;
same_pkt = 0;
suc_pkt_single = [0 0];
tran_time = 0;
ap_retrans = zeros(1,ap_num);
next_tran_time = zeros(1,ap_num);

for i = 1:ap_num % initial backoff time
next_tran_time(i) =floor(CWmin * rand) * slot_time;
end

while tran_time < 1000000
tran_time = min(next_tran_time);
no_tran = sum(tran_time == next_tran_time);

if no_tran == 1 % 传输成功
for i = 1:ap_num
if next_tran_time(i) == tran_time
suc_pkt_single(i) = suc_pkt_single(i) + 1;
suc_pkt = suc_pkt + 1;
if tran_time >= 1000000
sim_time = next_tran_time (i) + phy_header + mac_header + payload +
   SIFS + ACK + DIFS;
end
next_tran_time(i) = next_tran_time(i) + phy_header + mac_header +
   payload + SIFS+ACK+DIFS+floor(CWmin*rand)*slot_time;
else
next_tran_time(i) = next_tran_time(i) + phy_header + mac_header +
   payload + SIFS+ACK+DIFS;
end
end

else % 并发传输
suc_pkt = suc_pkt + 2;
same_pkt = same_pkt + 1;
if tran_time >= 1000000
sim_time = next_tran_time (i) + phy_header + mac_header + payload +
   SIFS + ACK + DIFS;
end
for i = 1:ap_num
suc_pkt_single(i) = suc_pkt_single(i) + 1;
if next_tran_time(i) == tran_time
next_tran_time(i) = next_tran_time(i) + phy_header + mac_header +
   payload + SIFS + ACK + DIFS + floor(CWmin*rand)*slot_time;


                                    40
```

[Visual fallback](page_images/page_041.jpg)

## Page 42

```text
end
end
end
end
throughput = [throughput physical_rate * suc_pkt * payload /
   sim_time];
throughput_ap1 = [throughput_ap1 physical_rate * suc_pkt_single(1) *
   payload / sim_time];
throughput_ap2 = [throughput_ap2 physical_rate * suc_pkt_single(2) *
   payload / sim_time];
same_num = [same_num same_pkt];
same_ratio = [same_ratio same_pkt / (suc_pkt - same_pkt)];
end

%% plot total throughput
plot(1:1:300,throughput,'LineWidth',1);
title('系统吞吐量','FontSize',15,'FontName','楷体');
xlabel('时间/s','FontSize',15,'FontName','楷体');
ylabel('吞吐量/Mbps','FontSize',15,'FontName','楷体');
saveas(gcf,
   ['C:\Users\A\Desktop\数学建模\problem2\totalThroughput.svg']);

%% plot single ap throughput
plot(1:1:300,throughput_ap1,1:1:300,throughput_ap2,'LineWidth',1);
title('单AP吞吐量','FontSize',15,'FontName','楷体');
xlabel('时间/s','FontSize',15,'FontName','楷体');
ylabel('吞吐量/Mbps','FontSize',15,'FontName','楷体');
l = legend('AP1','AP2');
set(l,'FontSize',12);
saveas(gcf,
   ['C:\Users\A\Desktop\数学建模\problem2\singleThroughput.svg']);

%% plot number of collision
% yyaxis left;
%
   plot(1:1:300,same_num,'LineWidth',1,'Color',[255/255,128/255,0/255]);
% title('碰撞数据包分析','FontSize',15,'FontName','楷体')
% xlabel('时间/s','FontSize',15,'FontName','楷体');
%
% yyaxis right;
%
   plot(1:1:300,same_ratio,'LineWidth',1,'Color',[64/255,105/255,224/255]);
% ylim([0,0.1]);
% legend('碰撞数量','碰撞比例','FontName','楷体');
% saveas(gcf,
   ['C:\Users\A\Desktop\数学建模\problem2\TransSameTimeNum.svg']);
% close all;
plot(1:1:300,same_ratio,'LineWidth',1,'Color',[64/255,105/255,224/255]);
title('并发传输情况','FontSize',15,'FontName','楷体');
xlabel('时间/s','FontSize',15,'FontName','楷体');
ylabel('并发比例','FontSize',15,'FontName','楷体');
saveas(gcf,
   ['C:\Users\A\Desktop\数学建模\problem2\TransSameTimeNum.svg']);
close all;


                                  41
```

[Visual fallback](page_images/page_042.jpg)

## Page 43

```text
%% plot cdf of throughput
[h, stats] = cdfplot(throughput);
title('经验CDF','FontSize',15,'FontName','楷体');
xlabel('吞吐量/Mbps','FontSize',15,'FontName','楷体');
saveas(gcf, ['C:\Users\A\Desktop\数学建模\problem2\troughoutCDF.svg']);


%% 问题三
clear;
clc;
close all;

%% Model Parameters
SIFS = 16; slot_time = 9; DIFS = 43; %us
payload_bits = 12000; mac_header_bits = 240; %bits
physical_rate = 455.8; %Mbps
payload = payload_bits / physical_rate; mac_header = mac_header_bits
   /physical_rate; %us
phy_header = 13.6; ACK = 32; ACKTimeout = 65; %us
%packet = payload + mac_header;
CWmin = 16;
m = 6;   %maxStage
r = 32; %maxRetransCnt
pe = 0.1;
sim_time = 0;
throughput = [];

%% Simulation
fprintf('Simulating...\n');
for sim_cnt = 1:300
ap_num = 2;
suc_pkt = 0;
cross_pkt = 0;
drop_pkt = 0;
ap_retrans = zeros(1,ap_num);
ap_stage = zeros(1,ap_num);
next_tran_time = zeros(1,ap_num);

for i = 1:ap_num % 初始化
next_tran_time(i) =floor(CWmin * rand) * slot_time;
end

while suc_pkt < 10000
[tran_time,idx_min]= min(next_tran_time);
[cross_time,idx_max] = max(next_tran_time);
cross_tran = abs(diff(next_tran_time)) > (phy_header + mac_header +
   payload + SIFS);

if cross_tran == 1 % 传输成功
if(rand > 0.1)
suc_pkt = suc_pkt + 1;
for i = 1:ap_num
if next_tran_time(i) == tran_time


                                    42
```

[Visual fallback](page_images/page_043.jpg)

## Page 44

```text
if suc_pkt == 10000
sim_time = next_tran_time (i) + phy_header + mac_header + payload +
   SIFS + ACK + DIFS;
end
ap_stage(i) = 0;
ap_retrans(i) = 0;
next_tran_time(i) = next_tran_time(i) + phy_header + mac_header +
   payload + SIFS+ACK+DIFS+floor(CWmin*rand)*slot_time;
end
end
else
drop_pkt = drop_pkt + 1;
if ap_stage(idx_min) < m
ap_stage(idx_min) = ap_stage(idx_min) + 1;
end
if ap_retrans(idx_min) < r
ap_retrans(idx_min) = ap_retrans(idx_min) + 1;
else
ap_stage(idx_min) = 0;
ap_retrans(idx_min) = 0;
end
for i = 1:ap_num
if next_tran_time(i) == tran_time
next_tran_time(i) = next_tran_time(i) + phy_header + mac_header +
   payload + ACKTimeout + DIFS +
   floor(2^ap_stage(i)*CWmin*rand)*slot_time;
end
end
end
else % 传输重叠
cross_pkt = cross_pkt + 2;
for i = 1:ap_num
if ap_stage(i) < m
ap_stage(i) = ap_stage(i) + 1;
end
if ap_retrans(i) < r
ap_retrans(i) = ap_retrans(i) + 1;
else
ap_stage(i) = 0;
ap_retrans(i) = 0;
end
end
if abs(next_tran_time(idx_max) - next_tran_time(idx_min)) > ACKTimeout
next_tran_time(idx_min) = next_tran_time(idx_max) + phy_header +
   mac_header + payload + DIFS +
   floor(2^ap_stage(idx_min)*CWmin*rand)*slot_time;
else
next_tran_time(idx_min) = next_tran_time(idx_min) + phy_header +
   mac_header + payload + ACKTimeout + DIFS +
   floor(2^ap_stage(idx_min)*CWmin*rand)*slot_time;
end
next_tran_time(idx_max) = next_tran_time(idx_max) + phy_header +
   mac_header + payload + ACKTimeout + DIFS +
   floor(2^ap_stage(idx_max)*CWmin*rand)*slot_time;


                                  43
```

[Visual fallback](page_images/page_044.jpg)

## Page 45

```text
end

end
throughput = [throughput physical_rate * suc_pkt * payload /
   sim_time];
end

%% plot total throughput
plot(1:1:300,throughput,'LineWidth',1);
title('系统吞吐量','FontSize',15,'FontName','楷体')
xlabel('时间/s','FontSize',15,'FontName','楷体');
ylabel('吞吐量/Mbps','FontSize',15,'FontName','楷体');
%saveas(gcf,
   ['C:\Users\A\Desktop\数学建模\problem3\totalThroughput6.svg']);
[h1, stats1] = cdfplot(throughput);


%% 问题四
clear;
clc;
close all;

%% Model Parameters
SIFS = 16; slot_time = 9; DIFS = 43; %us
payload_bits = 12000; mac_header_bits = 240; %bits
physical_rate = 455.8; %Mbps
payload = payload_bits / physical_rate; mac_header = mac_header_bits
   /physical_rate; %us
phy_header = 13.6; ACK = 32; ACKTimeout = 65; %us
%packet = payload + mac_header;
CWmin = 16;
m = 6;   %maxStage
r = 32; %maxRetransCnt
sim_time = 0;
throughput = [];
throughput_ap1 = [];
throughput_ap2 = [];
collision_num = [];
collision_ratio = [];

%% Simulation
fprintf('Simulating...\n');
for sim_cnt = 1:300
ap_num = 3;
suc_pkt = 0;
suc_pkt_single = [0 0 0];
tran_time = 0;
collision_pkt = 0;
cross_pkg = 0;
ap_stage = zeros(1,ap_num);
ap_retrans = zeros(1,ap_num);
next_tran_time = zeros(1,ap_num);

for i = 1:ap_num % 初始化


                                    44
```

[Visual fallback](page_images/page_045.jpg)

## Page 46

```text
ap_stage(i) = 0;
next_tran_time(i) =floor(CWmin * rand) * slot_time;
end

while tran_time < 1000000
if(next_tran_time(2) == next_tran_time(1) && next_tran_time(1) ==
   next_tran_time(3)) %先判断三节点是否会同时传输
collision_pkt = collision_pkt + 3;
for i = 1:ap_num
if ap_stage(i) < m
ap_stage(i) = ap_stage(i) + 1;
end
if ap_retrans(i) < r
ap_retrans(i) = ap_retrans(i) + 1;
else
ap_stage(i) = 0;
ap_retrans(i) = 0;
end
next_tran_time(i)=next_tran_time(i) + phy_header + mac_header +
   payload + ACKTimeout + DIFS +
   floor(2^ap_stage(i)*CWmin*rand)*slot_time;
end
end

[tran_time,idx_min] = min(next_tran_time); %求最早传输时间

if tran_time >= 1000000
sim_time = tran_time;
end

if idx_min == 1 %AP1先开始传输
if(next_tran_time(2) == next_tran_time(1)) %判断有无并发
no_tran = 1;
else
no_tran = 0;
end
cross_tran = abs(next_tran_time(3) - next_tran_time(1)) < (phy_header
   + mac_header + payload + SIFS); %判断有无交叠
if no_tran %有并发
collision_pkt = collision_pkt + 2;
for i = 1:ap_num
if next_tran_time(i) == tran_time
if ap_stage(i) < m
ap_stage(i) = ap_stage(i) + 1;
end
if ap_retrans(i) < r
ap_retrans(i) = ap_retrans(i) + 1;
else
ap_stage(i) = 0;
ap_retrans(i) = 0;
end
next_tran_time(i) = next_tran_time(i) + phy_header + mac_header +
   payload + ACKTimeout + DIFS +
   floor(2^ap_stage(i)*CWmin*rand)*slot_time;


                                  45
```

[Visual fallback](page_images/page_046.jpg)

## Page 47

```text
else
next_tran_time(i) = next_tran_time(i) + phy_header + mac_header +
   payload + DIFS;
end
end
elseif ~no_tran && ~cross_tran %无并发，无交叠
suc_pkt = suc_pkt + 1;
for i = 1:2
if next_tran_time(i) == tran_time
suc_pkt_single(i) = suc_pkt_single(i) + 1;
ap_stage(i) = 0;
ap_retrans(i) = 0;
next_tran_time(i) = next_tran_time(i) + phy_header + mac_header +
   payload + SIFS+ACK+DIFS+floor(2^ap_stage(i)*CWmin*rand)*slot_time;
else
next_tran_time(i) = next_tran_time(i) + phy_header + mac_header +
   payload + SIFS+ACK+DIFS;
end
end
elseif ~no_tran && cross_tran %无并发有交叠
cross_pkg = cross_pkg + 2;
suc_pkt = suc_pkt + 2;
next_tran_time(2) = next_tran_time(2) + floor(abs(next_tran_time(1) -
   next_tran_time(3))) + phy_header + mac_header + payload + SIFS +
   ACK + DIFS;
next_tran_time(1) = next_tran_time(1) + phy_header + mac_header +
   payload + SIFS + ACK + DIFS +
   floor(2^ap_stage(1)*CWmin*rand)*slot_time;
next_tran_time(3) = next_tran_time(3) + phy_header + mac_header +
   payload + SIFS + ACK + DIFS +
   floor(2^ap_stage(3)*CWmin*rand)*slot_time;
end
end

if idx_min == 2 %AP2先开始传输
no_tran = sum(tran_time == next_tran_time);
if no_tran == 1
suc_pkt = suc_pkt + 1;
for i = 1:ap_num
if next_tran_time(i) == tran_time
suc_pkt_single(i) = suc_pkt_single(i) + 1;
ap_stage(i) = 0;
ap_retrans(i) = 0;
next_tran_time(i) = next_tran_time(i) + phy_header + mac_header +
   payload + SIFS+ACK+DIFS+floor(2^ap_stage(i)*CWmin*rand)*slot_time;
else
next_tran_time(i) = next_tran_time(i) + phy_header + mac_header +
   payload + SIFS+ACK+DIFS;
end
end
else
collision_pkt = collision_pkt + 2;
for i = 1:ap_num
if next_tran_time(i) == tran_time


                                  46
```

[Visual fallback](page_images/page_047.jpg)

## Page 48

```text
if ap_stage(i) < m
ap_stage(i) = ap_stage(i) + 1;
end
if ap_retrans(i) < r
ap_retrans(i) = ap_retrans(i) + 1;
else
ap_stage(i) = 0;
ap_retrans(i) = 0;
end
next_tran_time(i)=next_tran_time(i) + phy_header + mac_header +
   payload + ACKTimeout + DIFS +
   floor(2^ap_stage(i)*CWmin*rand)*slot_time;
%          else
%             next_tran_time(i)=next_tran_time(i) + packet + DIFS;
else
next_tran_time(i) = next_tran_time(i) + phy_header + mac_header +
   payload + DIFS;
end
end
end
end

if idx_min == 3 %%AP3先开始传输
if(next_tran_time(2) == next_tran_time(3))
no_tran = 1;
else
no_tran = 0;
end
cross_tran = abs(next_tran_time(3) - next_tran_time(1)) < (phy_header
   + mac_header + payload + SIFS);
if no_tran
collision_pkt = collision_pkt + 2;
for i = 1:ap_num
if next_tran_time(i) == tran_time
if ap_stage(i) < m
ap_stage(i) = ap_stage(i) + 1;
end
if ap_retrans(i) < r
ap_retrans(i) = ap_retrans(i) + 1;
else
ap_stage(i) = 0;
ap_retrans(i) = 0;
end
next_tran_time(i) = next_tran_time(i) + phy_header + mac_header +
   payload + ACKTimeout + DIFS +
   floor(2^ap_stage(i)*CWmin*rand)*slot_time;
else
next_tran_time(i) = next_tran_time(i) + phy_header + mac_header +
   payload + DIFS;
end
end
elseif ~no_tran && ~cross_tran
suc_pkt = suc_pkt + 1;
for i = 2:3


                                  47
```

[Visual fallback](page_images/page_048.jpg)

## Page 49

```text
if next_tran_time(i) == tran_time
suc_pkt_single(i) = suc_pkt_single(i) + 1;
ap_stage(i) = 0;
ap_retrans(i) = 0;
next_tran_time(i) = next_tran_time(i) + phy_header + mac_header +
   payload + SIFS+ACK+DIFS+floor(2^ap_stage(i)*CWmin*rand)*slot_time;
else
next_tran_time(i) = next_tran_time(i) + phy_header + mac_header +
   payload + SIFS+ACK+DIFS;
end
end
elseif ~no_tran && cross_tran
cross_pkg = cross_pkg + 2;
suc_pkt = suc_pkt + 2;
next_tran_time(2) = next_tran_time(2) + floor(abs(next_tran_time(1) -
   next_tran_time(3))) + phy_header + mac_header + payload + SIFS +
   ACK + DIFS;
next_tran_time(1) = next_tran_time(1) + phy_header + mac_header +
   payload + SIFS + ACK + DIFS +
   floor(2^ap_stage(1)*CWmin*rand)*slot_time;
next_tran_time(3) = next_tran_time(3) + phy_header + mac_header +
   payload + SIFS + ACK + DIFS +
   floor(2^ap_stage(3)*CWmin*rand)*slot_time;
end
end


end
throughput = [throughput physical_rate * suc_pkt * payload /
   sim_time];
throughput_ap1 = [throughput_ap1 physical_rate * suc_pkt_single(1) *
   payload / sim_time];
throughput_ap2 = [throughput_ap2 physical_rate * suc_pkt_single(2) *
   payload / sim_time];
collision_num = [collision_num collision_pkt];
collision_ratio = [collision_ratio collision_pkt / (collision_pkt +
   suc_pkt)];
end

%% plot total throughput
plot(1:1:300,throughput,'LineWidth',1);
title('系统吞吐量','FontSize',15,'FontName','楷体')
xlabel('时间/s','FontSize',15,'FontName','楷体');
ylabel('吞吐量/Mbps','FontSize',15,'FontName','楷体');
saveas(gcf,
   ['C:\Users\A\Desktop\数学建模\problem4\totalThroughput0.svg']);
[h1, stats1] = cdfplot(throughput);




                                  48
```

[Visual fallback](page_images/page_049.jpg)
