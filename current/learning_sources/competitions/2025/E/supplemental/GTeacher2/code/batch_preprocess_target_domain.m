function batch_preprocess_target_domain()
clc; clear; close all;

%% ========= 配置区（按需修改） =========
input_folder   = 'E:\BaiduNetdiskDownload\数据集\数据集\目标域数据集';  % 输入目录
output_folder  = 'E:\BaiduNetdiskDownload\数据集\数据集\目标域数据集_预处理'; % 输出目录
plot_folder    = fullfile(output_folder, 'plots');  % 绘图输出目录（可视化对比）

if ~exist(output_folder, 'dir'); mkdir(output_folder); end
if ~exist(plot_folder, 'dir');   mkdir(plot_folder);   end

% 目标采样率（采样率对齐用）
target_fs      = 12000;     % 如需改为 12 kHz 对齐

% 初始宽带通滤波范围（先粗滤，后续会用谱峭度再精调）
init_bp        = [50, 8000];  % Hz，依据实际轴承与传感器带宽调整

% 谱峭度(STFT)参数（用于自动选带）
sk_win_len     = 1024;     % STFT 窗长（功率2次幂）
sk_overlap     = 0.75;     % 重叠比例
max_bp_bw      = 3000;     % 自动选带的最大带宽上限（Hz）
min_bp_bw      = 200;      % 自动选带的最小带宽下限（Hz）

% 估计转频 fr 的搜索范围（包络谱中找峰）
fr_search_Hz   = [1, 120]; % 依据列车轴频预估范围（单位 Hz），可调整

% 图像开关（每个文件画一张“原始 vs 滤波 vs 包络谱/阶次谱”对比）
enable_plot    = true;

%% =============== 批处理开始 ===============
files = dir(fullfile(input_folder, '*.mat'));
if isempty(files)
    warning('在目录中未找到 .mat 文件：%s', input_folder);
    return;
end

for k = 1:numel(files)
    in_path = fullfile(files(k).folder, files(k).name);
    S = load(in_path);

    % ------ 自动推断原始数据与采样率 ------
    [x, fs] = infer_signal_and_fs(S);
    if isempty(x)
        fprintf('[跳过] %s：未能识别到有效信号向量。\n', files(k).name);
        continue;
    end
    x = double(x(:)); % 统一成列向量
    if isempty(fs)
        fs = 32000; % 没有提供 fs 时的默认值（按需改）
        fprintf('[提示] %s：未检测到 fs，默认 fs = %d Hz。\n', files(k).name, fs);
    end

    % ------ 初始带通滤波（粗降噪）------
    init_bp_clamped = [max(1, init_bp(1)), min(init_bp(2), fs/2-100)];
    d0 = designfilt('bandpassiir', 'FilterOrder', 4, ...
        'HalfPowerFrequency1', init_bp_clamped(1), ...
        'HalfPowerFrequency2', init_bp_clamped(2), ...
        'SampleRate', fs);
    x_bp = filtfilt(d0, x);

    % ------ 谱峭度选带（自动聚焦故障共振带）------
    [bp1, bp2] = auto_band_by_spectral_kurtosis(x_bp, fs, sk_win_len, sk_overlap, min_bp_bw, max_bp_bw);
    % 防越界与宽度保护
    bp1 = max(1, bp1); 
    bp2 = min(fs/2-50, bp2);
    if bp2 <= bp1
        % 退化处理：使用初始带通
        bp1 = init_bp_clamped(1);
        bp2 = init_bp_clamped(2);
    end
    d1 = designfilt('bandpassiir', 'FilterOrder', 4, ...
        'HalfPowerFrequency1', bp1, ...
        'HalfPowerFrequency2', bp2, ...
        'SampleRate', fs);
    x_sk = filtfilt(d1, x_bp);

    % ------ Hilbert 包络解调 ------
    env = abs(hilbert(x_sk));

    % ------ 重采样（采样率对齐）------
    if fs ~= target_fs
        [P, Q] = rat(target_fs / fs);
        x_resampled   = resample(x_sk, P, Q);
        env_resampled = resample(env,   P, Q);
        fs_new        = target_fs;
    else
        x_resampled   = x_sk;
        env_resampled = env;
        fs_new        = fs;
    end

    % ------ 包络谱 & 转频估计（用于阶次分析）------
    [f_env, P_env] = one_sided_psd(env_resampled, fs_new);
    % 在设定范围内找包络谱主峰，估计转频 fr
    idx_band = f_env >= fr_search_Hz(1) & f_env <= fr_search_Hz(2);
    [~, iMax] = max(P_env(idx_band));
    fr_est = f_env(find(idx_band,1,'first') + iMax - 1); % 估计轴频 Hz

    % ------ 阶次谱（基于 fr_est 将频率轴换算为阶次轴）------
    orders = f_env / max(fr_est, eps); % 1阶 = fr_est
    % 为了可视化平滑一些阶次谱
    P_order = P_env;

    % ------ 保存结果 ------
    out_name = erase(files(k).name, '.mat');
    save_path = fullfile(output_folder, [out_name '_proc.mat']);
    meta = struct();
    meta.file_name   = files(k).name;
    meta.fs_original = fs;
    meta.fs_target   = fs_new;
    meta.init_band   = init_bp_clamped;
    meta.sk_band     = [bp1, bp2];
    meta.fr_est      = fr_est;     % 估计转频(Hz)
    meta.note        = 'x_proc：谱峭度选带后的信号（若已重采样则为 target_fs）；env_proc：Hilbert 包络；f_env/P_env：包络谱；orders/P_order：阶次谱';

    x_proc   = x_resampled;
    env_proc = env_resampled;

    save(save_path, 'x_proc', 'env_proc', 'fs_new', 'f_env', 'P_env', 'orders', 'P_order', 'meta');
    fprintf('[完成] %s -> %s（选带[%.0f %.0f]Hz，fr≈%.2fHz）\n', ...
        files(k).name, save_path, bp1, bp2, fr_est);

    % ------ 可视化（可选）------
    if enable_plot
        try
            fig = figure('Visible','off','Position',[100 100 1100 800]);
            t_raw = (0:numel(x)-1)/fs;
            t_new = (0:numel(x_proc)-1)/fs_new;

            subplot(3,2,1); 
            plot(t_raw, x); grid on; xlim([0, min(2, t_raw(end))]);
            title('原始信号（截取前2s）'); xlabel('Time (s)'); ylabel('Amplitude');

            subplot(3,2,2);
            plot(t_raw, x_bp); hold on; plot(t_raw, x_sk); grid on; xlim([0, min(2, t_raw(end))]);
            legend('初始带通','谱峭度选带后'); 
            title(sprintf('带通处理：初始[%d,%d]Hz → SK选带[%.0f,%.0f]Hz', ...
                init_bp_clamped(1), init_bp_clamped(2), bp1, bp2));
            xlabel('Time (s)'); ylabel('Amplitude');

            subplot(3,2,3);
            plot(t_new, env_proc); grid on; xlim([0, min(2, t_new(end))]);
            title('Hilbert 包络（截取前2s）'); xlabel('Time (s)'); ylabel('Envelope');

            subplot(3,2,4);
            plot(f_env, P_env); grid on; xlim([0, min(500, f_env(end))]);
            hold on; xline(fr_est, '--r', sprintf(' fr=%.2f Hz ', fr_est));
            title('包络谱'); xlabel('Frequency (Hz)'); ylabel('Power');

            subplot(3,2,5);
            plot(orders, P_order); grid on; xlim([0, 20]); % 只看前20阶
            title('阶次谱（1阶 = fr）'); xlabel('Order'); ylabel('Power');

            subplot(3,2,6);
            spectrogram_quick(x_proc, fs_new);
            title('处理后信号的时频图（参考）');

            saveas(fig, fullfile(plot_folder, [out_name '_preview.png']));
            close(fig);
        catch ME
            warning('绘图失败：%s | %s', files(k).name, ME.message);
        end
    end
end

disp('=== 全部文件处理完成 ===');

end % function

%% --------- 工具函数：自动识别信号与采样率 ---------
function [x, fs] = infer_signal_and_fs(S)
x = [];
fs = [];

% 常见变量名猜测（你可按自己数据实际改这里的优先级）
cand_signal = {'x','sig','signal','data','vibration','acc','accX','Ch1','raw_signal','y'};
cand_fs     = {'fs','Fs','sample_rate','sampling_rate','SR','sr'};

% 找信号
fn = fieldnames(S);
for i = 1:numel(cand_signal)
    if ismember(cand_signal{i}, fn)
        xi = S.(cand_signal{i});
        if isnumeric(xi) && ~isempty(xi)
            % 多通道默认取第一列
            if size(xi,2) > 1, xi = xi(:,1); end
            x = xi; break;
        end
    end
end
% 若仍未找到，尝试：第一个数值长向量
if isempty(x)
    for i = 1:numel(fn)
        vi = S.(fn{i});
        if isnumeric(vi) && isvector(vi) && numel(vi) >= 1000
            if size(vi,2) > 1, vi = vi(:,1); end
            x = vi; break;
        end
    end
end

% 找采样率
for i = 1:numel(cand_fs)
    if ismember(cand_fs{i}, fn)
        fsi = S.(cand_fs{i});
        if isnumeric(fsi) && isscalar(fsi) && fsi > 0
            fs = double(fsi); break;
        end
    end
end
end

%% --------- 工具函数：谱峭度选带（基于STFT的简化实现） ---------
function [bp1, bp2] = auto_band_by_spectral_kurtosis(x, fs, win_len, overlap_ratio, min_bw, max_bw)
% 计算短时傅里叶变换
noverlap = round(win_len * overlap_ratio);
[S,F,~]  = spectrogram(x, hann(win_len,'periodic'), noverlap, win_len, fs, 'yaxis');
A  = abs(S);           % 幅度谱（time x freq）
A  = A.';              % 维度：freq x time
% 每个频率bin在时间轴上的峭度（kurtosis）
Kf = kurtosis(A, 0, 2);  % freq 方向得到一条曲线

% 找峰值频率作为中心
[~, imax] = max(Kf);
f0 = F(imax);
% 自适应带宽：在 Kf 半高宽范围内截取，限制在[min_bw, max_bw]
% 找到半高点
half = (Kf(imax) + median(Kf))/2;
left  = imax; while left>1   && Kf(left)  > half, left  = left-1; end
right = imax; while right<numel(F) && Kf(right) > half, right = right+1; end
bw_est = F(right) - F(left);
bw_est = min(max(bw_est, min_bw), max_bw);

bp1 = max(1, f0 - bw_est/2);
bp2 = min(fs/2 - 50, f0 + bw_est/2);
end

%% --------- 工具函数：单边功率谱 ---------
function [f, Pxx] = one_sided_psd(x, fs)
N = numel(x);
Nfft = 2^nextpow2(N);
X = fft(x, Nfft);
P2 = abs(X/Nfft).^2;             % 双边功率谱（简化）
P1 = P2(1:Nfft/2+1);
P1(2:end-1) = 2*P1(2:end-1);     % 单边
f = fs*(0:(Nfft/2))/Nfft;
Pxx = P1;
end

%% --------- 工具函数：快速时频图 ---------
function spectrogram_quick(x, fs)
win = hann(1024,'periodic'); 
noverlap = round(numel(win)*0.75);
[S,F,T] = spectrogram(x, win, noverlap, 1024, fs, 'yaxis');
imagesc(T, F, 20*log10(abs(S)+eps)); axis xy; colorbar;
xlabel('Time (s)'); ylabel('Frequency (Hz)');
end
