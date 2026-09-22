function plot_fusion_results()
%% ==== 1) 自动定位 Excel ====
cands = { ...
    'E:\桌面\dg\sxjm2\提交\第三问\画图\新建文件夹\融合结果_from_quick.xlsx', ...
};
excel_file = '';
for i = 1:numel(cands)
    if exist(cands{i},'file'); excel_file = cands{i}; break; end
end
assert(~isempty(excel_file), '未找到融合结果 Excel，请检查路径。');

sheet_name = 'fusion';  % 目标工作表

%% ==== 2) 读取数据（大小写/命名鲁棒） ====
T = readtable(excel_file, 'Sheet', sheet_name);
vn = lower(T.Properties.VariableNames);

% 小工具：找列（用 contains 兜底）
getcol = @(key) T.(T.Properties.VariableNames{find(strcmp(vn,key) | contains(vn,key),1)});

sample   = string(getcol('sample'));
conf1    = double(getcol('confmaj_1'));   % run1 置信度
conf2    = double(getcol('confmaj_2'));   % run2 置信度
confF    = double(getcol('finalconf'));   % 融合置信度
labF     = upper(strtrim(string(getcol('finallabel'))));
agreeVec = double(getcol('agree'));

% 排序（若包含完整 A..P 按字母，否则保持原顺序）
wantOrder = string('A':'P')';
if all(ismember(wantOrder, sample))
    [~,ord] = ismember(sample, wantOrder);
    [~,idx] = sort(ord);
else
    idx = 1:numel(sample);
end
sample = sample(idx); conf1 = conf1(idx); conf2 = conf2(idx);
confF  = confF(idx);  labF  = labF(idx);  agreeVec = agreeVec(idx);

%% ==== 3) 公共设置 ====
faultSet = ["OR","IR","B"];
isFault  = ismember(labF, faultSet);
outdir   = fileparts(excel_file); if isempty(outdir), outdir = pwd; end
set(groot,'defaultAxesFontName','微软雅黑');
set(groot,'defaultTextFontName','微软雅黑');

%% ==== 4) 图1：每个样本置信度对比（分组柱状图） ====
fig1 = figure('Color','w','Position',[100 100 1200 420]);
X = (1:numel(sample))';
Y = [conf1 conf2 confF];
bar(X, Y, 'grouped', 'LineWidth', 0.8);
grid on; ylim([0 1]); yticks(0:0.1:1);
xticks(X); xticklabels(sample); xtickangle(0);
ylabel('置信度');
title('两次预测与最终融合置信度对比');
legend({'ConfMaj\_1','ConfMaj\_2','FinalConf'}, 'Location','southoutside','Orientation','horizontal');

% 在每组上方标注最终标签
for i = 1:numel(sample)
    ytop = min(1, max(Y(i,:)) + 0.02);
    text(X(i), ytop, labF(i), 'HorizontalAlignment','center','FontSize',9);
end
saveas(fig1, fullfile(outdir, '图1_置信度对比.png'));

%% ==== 5) 图2：散点（仅显示一致 vs 不一致） ====
fig2 = figure('Color','w','Position',[100 580 600 520]);
hold on; grid on; box on

% 颜色与标记
cDisagree = [0.00 0.45 0.74];   % 不一致：蓝色圆点
cAgree    = [0.85 0.33 0.10];   % 一致：橙色三角
ms0 = 60; ms1 = 70;

idx0 = (agreeVec==0);   % 不一致
idx1 = (agreeVec==1);   % 一致

% 两类点
h0 = scatter(conf1(idx0), conf2(idx0), ms0, cDisagree, 'o', 'filled', 'MarkerFaceAlpha',0.7);
h1 = scatter(conf1(idx1), conf2(idx1), ms1, cAgree,    '^', 'filled', 'MarkerFaceAlpha',0.9);

% 可选：在点旁标注样本名（A..P），需要就把 addLabels 设为 true
addLabels = true;
if addLabels
    for i = 1:numel(sample)
        text(conf1(i)+0.01, conf2(i), sample(i), 'FontSize',9, 'Color',[0.15 0.15 0.15]);
    end
end

% 参考线 y=x
plot([0 1],[0 1],'k--','LineWidth',1);

% 轴与标题
xlim([0 1]); ylim([0 1]); xticks(0:0.1:1); yticks(0:0.1:1);
xlabel('ConfMaj\_1'); ylabel('ConfMaj\_2');
title('两次预测置信度散点图');

% 简洁图例
legend([h0 h1], {'不一致','一致'}, 'Location','southeast');

hold off
saveas(fig2, fullfile(outdir, '图2_散点_Conf1_vs_Conf2.png'));


%% ==== 6) 图3：最终标签分布（计数柱状图） ====
fig3 = figure('Color','w','Position',[740 580 560 520]);

labsExisting = categories(categorical(upper(strtrim(labF))));
prefRow = ["OR","IR","B","N","UNK"];
labsRow = string(labsExisting(:)).';
allLabs = unique([prefRow, labsRow], 'stable');


C   = categorical(upper(strtrim(labF)), allLabs, 'Ordinal', true);
cnt = countcats(C);

bar(cnt, 'LineWidth', 0.8, 'FaceColor',[0.3 0.3 0.9]); grid on
set(gca, 'XTick', 1:numel(allLabs), 'XTickLabel', allLabs);
ylabel('数量');

agree_rate = mean(agreeVec) * 100;
title(sprintf('最终标签分布', agree_rate));

ymax = max([cnt; 1]);
for i = 1:numel(cnt)
    text(i, cnt(i) + 0.02*ymax, string(cnt(i)), 'HorizontalAlignment','center','FontSize',9);
end
saveas(fig3, fullfile(outdir, '图3_最终标签分布.png'));

fprintf('✅ 已输出图片至：%s\n', outdir);
end
