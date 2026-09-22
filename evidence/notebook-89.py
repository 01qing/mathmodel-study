# CELL 0
import os, re, glob, json, math, random, warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from scipy.io import loadmat
from scipy import signal
from scipy.signal import butter, filtfilt, hilbert
from scipy.stats import kurtosis, skew
import pywt

from sklearn.preprocessing import MinMaxScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
from sklearn.model_selection import train_test_split, StratifiedKFold
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay, accuracy_score, f1_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.inspection import permutation_importance, PartialDependenceDisplay

import shap

warnings.filterwarnings("ignore")
plt.rcParams["figure.dpi"] = 120
plt.rcParams["savefig.dpi"] = 300
plt.rcParams["axes.grid"] = True
plt.rcParams["grid.alpha"] = 0.22
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams["font.sans-serif"] = ['Kaiti']
plt.rcParams["axes.unicode_minus"] = False

TARGET_FS      = 12000         # 统一采样率
SEG_LEN        = 2048          # 分段长度
HOP_LEN        = SEG_LEN       # 非重叠
BP_LOW         = 100.0         # 带通下限
NB_WIDTH_HZ    = 5.0           # 理论频率窄带半宽（±5Hz）
CHANNELS_TO_USE= ["DE","FE"]   # 通道优先级（若仅 UNK 则仍会处理）
TSNE_SUBSAMPLE = 2000          # t-SNE 最多使用样本（避免过慢）；None 表示不限制
RANDOM_STATE   = 42
MAX_FILES      = None          # 例如 60
MAX_SEGMENTS   = None          # 每文件最多片段数，例如 60

# 输出路径
CSV_FEATURES_RAW = "源域特征_原始统计.csv"
CSV_FEATURES_PCA = "源域特征_PCA95.csv"
JSON_PREPROC     = "特征预处理配置.json"

def bandpass_filter(x, fs, low=100.0, high=None, order=4):
    nyq = 0.5*fs
    if high is None:
        high = min(5000.0, 0.45*fs)
    lowc  = max(low/nyq, 1e-6)
    highc = min(high/nyq, 0.999)
    if highc <= lowc:
        highc = min(0.999, lowc + 1e-3)
    b,a = butter(order, [lowc, highc], btype="band")
    return filtfilt(b, a, x)

def wavelet_denoise(x, wavelet="db4", level=None):
    if level is None:
        level = min(5, pywt.dwt_max_level(len(x), pywt.Wavelet(wavelet).dec_len))
    coeffs = pywt.wavedec(x, wavelet, level=level, mode='symmetric')
    sigma  = np.median(np.abs(coeffs[-1]))/0.6745 + 1e-12
    thr    = sigma*np.sqrt(2*np.log(len(x)))
    den    = [coeffs[0]] + [pywt.threshold(c, thr, mode="soft") for c in coeffs[1:]]
    out    = pywt.waverec(den, wavelet, mode='symmetric')
    return out[:len(x)]

pats = ["**/*.mat", "**/*.csv", "**/*.txt", "**/*.npy"]
files = []
for p in pats:
    files += glob.glob(os.path.join(".", p), recursive=True)
files = [f for f in files if not os.path.basename(f).lower().endswith((".png",".jpg",".jpeg",".csv",".json",".pdf",".doc",".docx",".ppt",".pptx"))]
files = [f for f in files if "/." not in f.replace("\\",".")]
files = sorted(files)
if MAX_FILES is not None:
    files = files[:MAX_FILES]

def infer_fs_from_name(name, default=None):
    s = name.lower()
    m1 = re.search(r'(\d+)\s*k\s*hz?', s)
    if m1: return int(m1.group(1))*1000
    m2 = re.search(r'fs[_\-]?\s*(\d+)', s)
    if m2:
        v=int(m2.group(1)); return v if v>100 else v*1000
    m3 = re.findall(r'(\d{4,6})', s)
    for g in m3:
        v=int(g)
        if 2000<=v<=200000: return v
    if "12k" in s: return 12000
    if "32k" in s: return 32000
    if "48k" in s: return 48000
    return default

def infer_label_from_path(path):
    s = path.lower()
    if re.search(r'(^|[^a-z])or([^a-z]|$)|outer', s): return "OR"
    if re.search(r'(^|[^a-z])ir([^a-z]|$)|inner', s): return "IR"
    if re.search(r'ball|(^|[^a-z])b([^a-z]|$)', s):   return "B"
    if re.search(r'normal|(^|[^a-z])n([^a-z]|$)', s): return "N"
    if "外圈" in s: return "OR"
    if "内圈" in s: return "IR"
    if "滚动体" in s: return "B"
    if "正常"  in s or "无故障" in s: return "N"
    return "UNK"

def load_from_mat(path):
    try:
        m = loadmat(path)
    except Exception:
        return {}, None
    channels, rpm_val = {}, None
    for k, v in m.items():
        if "rpm" in k.lower():
            arr = np.array(v).reshape(-1)
            arr = arr[np.isfinite(arr)]
            if arr.size>0: rpm_val = float(np.median(arr)); break
    for k, v in m.items():
        if k.startswith("__"): continue
        arr = np.array(v)
        if not np.issubdtype(arr.dtype, np.number): continue
        arr = arr.reshape(-1)
        if arr.size < SEG_LEN*2: continue
        keyl = k.lower(); ch=None
        if "de" in keyl: ch="DE"
        elif "fe" in keyl: ch="FE"
        elif "ba" in keyl: ch="BA"
        else:
            if re.search(r'[_\-]de[_\-]|de[_\-]time', keyl): ch="DE"
            elif re.search(r'[_\-]fe[_\-]|fe[_\-]time', keyl): ch="FE"
            elif re.search(r'[_\-]ba[_\-]|ba[_\-]time', keyl): ch="BA"
        if ch is None: continue
        cur = channels.get(ch)
        if (cur is None) or (arr.size > cur.size):
            channels[ch] = arr.astype(np.float64)
    return channels, rpm_val

def load_generic(path):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".npy":
        try:
            arr = np.load(path).reshape(-1).astype(np.float64)
            return {"UNK": arr}, None
        except:
            return {}, None
    try:
        try:
            df = pd.read_csv(path, engine="python")
        except Exception:
            df = pd.read_csv(path, sep=None, engine="python")
    except Exception:
        try:
            df = pd.read_csv(path, sep=r"[\s,;]+", engine="python", header=None)
        except:
            return {}, None
    for col in df.columns:
        s = pd.to_numeric(df[col], errors="coerce")
        if s.notna().sum() > len(s)*0.5:
            return {"UNK": s.dropna().astype(np.float64).values}, None
    s = pd.to_numeric(df.iloc[:,0], errors="coerce").dropna().astype(np.float64)
    return {"UNK": s.values}, None

feature_rows = []
plot_samples = []  # 存少量段用于后续画图
random.seed(RANDOM_STATE)

for idx, path in enumerate(files, 1):
    ext = os.path.splitext(path)[1].lower()
    label_guess = infer_label_from_path(path)
    fs_guess    = infer_fs_from_name(os.path.basename(path), default=TARGET_FS)

    if ext == ".mat":
        ch_dict, rpm = load_from_mat(path)
    else:
        ch_dict, rpm = load_generic(path)

    if not ch_dict:
        continue
    if set(ch_dict.keys()) != {"UNK"} and CHANNELS_TO_USE:
        ch_dict = {k:v for k,v in ch_dict.items() if k in CHANNELS_TO_USE}
        if not ch_dict:
            continue
    for ch_name, sig in ch_dict.items():
        fs_used = fs_guess if fs_guess is not None else TARGET_FS
        if fs_used != TARGET_FS:
            try:
                sig = signal.resample_poly(sig, TARGET_FS, int(fs_used))
            except Exception:
                new_len = int(round(len(sig)*TARGET_FS/float(fs_used)))
                sig = signal.resample(sig, new_len)
            fs_used = TARGET_FS

        if len(sig) < SEG_LEN*2:
            continue
        segs = []
        for st in range(0, len(sig)-SEG_LEN+1, HOP_LEN):
            segs.append(sig[st:st+SEG_LEN])
            if MAX_SEGMENTS is not None and len(segs)>=MAX_SEGMENTS:
                break
        segs = np.array(segs)
        for j, seg in enumerate(segs):
            x = bandpass_filter(seg, fs_used, BP_LOW, min(5000.0, 0.45*fs_used))
            x = wavelet_denoise(x, "db4")
            ptp = np.ptp(x)
            x = np.zeros_like(x) if ptp<1e-12 else 2*(x - np.min(x))/ptp - 1

            rms = np.sqrt(np.mean(x**2) + 1e-12)
            mean_abs = np.mean(np.abs(x)) + 1e-12
            peak = np.max(np.abs(x)) + 1e-12
            feats = {
                "td_mean": float(np.mean(x)),
                "td_std": float(np.std(x)),
                "td_rms": float(rms),
                "td_skew": float(skew(x)),
                "td_kurt": float(kurtosis(x, fisher=False)),
                "td_peak": float(peak),
                "td_peak2peak": float(np.ptp(x)),
                "td_crest_factor": float(peak/rms),
                "td_shape_factor": float(rms/mean_abs),
                "td_impulse_factor": float(peak/mean_abs),
                "td_margin_factor": float(peak / (np.mean(np.sqrt(np.abs(x))+1e-12)**2 + 1e-12)),
            }
            N = len(x)
            X = np.fft.rfft(x*np.hanning(N))
            freqs = np.fft.rfftfreq(N, d=1.0/fs_used)
            power = (np.abs(X)**2)/N
            total = np.sum(power)+1e-12
            centroid = np.sum(freqs*power)/total
            spread = np.sqrt(np.sum((freqs-centroid)**2 * power)/total)
            flatness = np.exp(np.mean(np.log(power+1e-12)))/(np.mean(power)+1e-12)
            idx_top = np.argpartition(power, -5)[-5:]
            idx_top = idx_top[np.argsort(freqs[idx_top])]
            feats.update({
                "spec_total_power": float(total),
                "spec_centroid": float(centroid),
                "spec_spread": float(spread),
                "spec_flatness": float(flatness),
                "spec_peak_freq": float(freqs[np.argmax(power)]),
            })
            for k, ii in enumerate(idx_top[-3:]):
                feats[f"spec_top{k+1}_freq"]  = float(freqs[ii])
                feats[f"spec_top{k+1}_power"] = float(power[ii])

            env = np.abs(hilbert(x - np.mean(x)))
            N2 = len(env)
            XE = np.fft.rfft((env-np.mean(env))*np.hanning(N2))
            fE = np.fft.rfftfreq(N2, d=1.0/fs_used)
            pE = (np.abs(XE)**2)/N2
            totalE = np.sum(pE)+1e-12
            idx_e = np.argpartition(pE, -3)[-3:]
            idx_e = idx_e[np.argsort(fE[idx_e])]
            feats.update({
                "env_total_power": float(totalE),
                "env_centroid": float(np.sum(fE*pE)/totalE),
                "env_peak_freq": float(fE[np.argmax(pE)]),
            })
            for k, ii in enumerate(idx_e):
                feats[f"env_top{k+1}_freq"]  = float(fE[ii])
                feats[f"env_top{k+1}_power"] = float(pE[ii])

            wp = pywt.WaveletPacket(x, wavelet="db4", maxlevel=3, mode="symmetric")
            nodes = [n.path for n in wp.get_level(3, order="freq")]
            energies = np.array([np.sum(wp[p].data**2) for p in nodes], dtype=float)
            probs = energies/(np.sum(energies)+1e-12)
            ent = -np.sum(probs*np.log(probs+1e-12))
            feats["wp_entropy"] = float(ent)
            for ii, e in enumerate(probs):
                feats[f"wp_e_{ii}"] = float(e)

            feats["path"]    = path
            feats["channel"] = ch_name
            feats["label"]   = label_guess
            feats["fs_used"] = fs_used
            feats["seg_idx"] = j
            feature_rows.append(feats)

            if len(plot_samples) < 6 and random.random() < 0.2:
                plot_samples.append((seg.copy(), x.copy(), fs_used, os.path.basename(path), ch_name, j, (fE, pE)))

feat_df = pd.DataFrame(feature_rows).replace([np.inf,-np.inf], np.nan).fillna(0.0)
feat_df.to_csv(CSV_FEATURES_RAW, index=False, encoding="utf-8-sig")

display(feat_df.head(10))
plt.figure(figsize=(8.2,4.5))
(feat_df["label"].value_counts().sort_index()).plot(kind="bar", width=0.8)
plt.title("样本类别分布（分段计数）")
plt.xlabel("标签")
plt.ylabel("数量")
plt.tight_layout()
plt.savefig("样本类别分布.png")
plt.show()

feature_cols = [c for c in feat_df.columns if c not in ["path","channel","label","fs_used","seg_idx"]]
scaler = MinMaxScaler()
X_scaled = scaler.fit_transform(feat_df[feature_cols].values)

pca = PCA(n_components=0.95, svd_solver="full", random_state=RANDOM_STATE)
X_pca = pca.fit_transform(X_scaled)
pca_cols = [f"pc{i+1}" for i in range(X_pca.shape[1])]
final_df = pd.concat([feat_df[["path","channel","label","fs_used","seg_idx"]].reset_index(drop=True),
                      pd.DataFrame(X_pca, columns=pca_cols)], axis=1)
final_df.to_csv(CSV_FEATURES_PCA, index=False, encoding="utf-8-sig")
print(">>> 已保存 PCA95% 特征：", CSV_FEATURES_PCA, "形状：", final_df.shape)
display(final_df.head(10))

preproc_cfg = {
    "scaler": {"data_min_": scaler.data_min_.tolist(), "data_max_": scaler.data_max_.tolist()},
    "pca": {"n_components_": int(X_pca.shape[1]), "explained_variance_ratio_": pca.explained_variance_ratio_.tolist()},
    "feature_cols": feature_cols,
    "target_fs": TARGET_FS, "seg_len": SEG_LEN, "hop_len": HOP_LEN,
    "nb_width_hz": NB_WIDTH_HZ, "channels_used": CHANNELS_TO_USE
}
with open(JSON_PREPROC, "w", encoding="utf-8") as f:
    json.dump(preproc_cfg, f, ensure_ascii=False, indent=2)

plt.figure(figsize=(8.4,4.6))
ratios = pca.explained_variance_ratio_
cum    = np.cumsum(ratios)
plt.bar(range(1, len(ratios)+1), ratios, label="单成分贡献")
plt.plot(range(1, len(ratios)+1), cum, marker="o", label="累计贡献")
plt.xlabel("主成分编号")
plt.ylabel("方差贡献率")
plt.title("PCA 方差贡献率（保留≥95%）")
plt.legend()
plt.tight_layout()
plt.savefig("PCA方差贡献率.png")
plt.show()

X_tsne_in = X_pca[:, :min(X_pca.shape[1], 50)]
labels_all = final_df["label"].values
if TSNE_SUBSAMPLE is not None and len(X_tsne_in) > TSNE_SUBSAMPLE:
    random.seed(RANDOM_STATE)
    idxs = sorted(random.sample(range(len(X_tsne_in)), TSNE_SUBSAMPLE))
    X_tsne_use = X_tsne_in[idxs]
    labels_use = labels_all[idxs]
else:
    X_tsne_use = X_tsne_in
    labels_use = labels_all

tsne = TSNE(n_components=2, perplexity=30, learning_rate="auto", init="pca",
            random_state=RANDOM_STATE, n_iter=1000)
X_tsne = tsne.fit_transform(X_tsne_use)

uniq_labels = sorted(list(set(labels_use)))
cmap = plt.cm.get_cmap("tab10", len(uniq_labels))
plt.figure(figsize=(9,6))
for i, lb in enumerate(uniq_labels):
    mask = (labels_use == lb)
    plt.scatter(X_tsne[mask,0], X_tsne[mask,1], s=18, alpha=0.85, label=str(lb), c=np.array([cmap(i)]))
plt.xlabel("t-SNE 1")
plt.ylabel("t-SNE 2")
plt.title("t-SNE（基于PCA特征）")
plt.legend(title="标签", bbox_to_anchor=(1.02, 1), loc="upper left", frameon=False)
plt.tight_layout()
plt.savefig("tSNE_PCA特征.png")
plt.show()

def quick_spectrum(x, fs):
    N = len(x)
    X = np.fft.rfft(x*np.hanning(N))
    f = np.fft.rfftfreq(N, d=1.0/fs)
    p = (np.abs(X)**2)/N
    return f, p

for k, (seg_raw, x_proc, fs_used, fname, ch, seg_idx, env_spec) in enumerate(plot_samples[:6], 1):
    # 原始
    t = np.arange(len(seg_raw))/fs_used
    plt.figure(figsize=(9,3.6))
    plt.plot(t, seg_raw, lw=1.0)
    plt.xlabel("时间 (s)"); plt.ylabel("幅值")
    plt.title(f"示例{k} | {fname} | {ch} | seg#{seg_idx} - 原始波形")
    plt.tight_layout(); plt.savefig(f"示例{k}_{ch}_seg{seg_idx}_原始波形.png"); plt.show()

    f, p = quick_spectrum(seg_raw, fs_used)
    plt.figure(figsize=(9,3.6))
    plt.semilogy(f, p, lw=1.0)
    plt.xlabel("频率 (Hz)"); plt.ylabel("功率谱密度(相对)")
    plt.title(f"示例{k} - 功率谱")
    plt.tight_layout(); plt.savefig(f"示例{k}_{ch}_seg{seg_idx}_功率谱.png"); plt.show()

    fE, pE = env_spec
    plt.figure(figsize=(9,3.6))
    plt.semilogy(fE, pE, lw=1.0, label="包络谱")
    plt.xlabel("频率 (Hz)"); plt.ylabel("幅度 (相对)")
    plt.title(f"示例{k} - 包络谱")
    plt.tight_layout(); plt.savefig(f"示例{k}_{ch}_seg{seg_idx}_包络谱.png"); plt.show()

mask_known = feat_df["label"].isin(["OR","IR","B","N"])
df_raw = feat_df[mask_known].reset_index(drop=True)
df_pca = final_df[mask_known].reset_index(drop=True)

y = df_raw["label"].values
X_raw = df_raw[feature_cols].values
X_pca = df_pca[pca_cols].values

Xtr_raw, Xte_raw, ytr, yte = train_test_split(X_raw, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y)
Xtr_pca, Xte_pca, _,  _   = train_test_split(X_pca, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y)

rf_raw = RandomForestClassifier(n_estimators=400, max_depth=None, random_state=RANDOM_STATE, n_jobs=-1, class_weight="balanced")
rf_raw.fit(Xtr_raw, ytr)
pred_raw = rf_raw.predict(Xte_raw)
print("【RF-原始特征】")
print(classification_report(yte, pred_raw, digits=4))
acc_raw = accuracy_score(yte, pred_raw); f1_raw = f1_score(yte, pred_raw, average="macro")
print(f"Accuracy={acc_raw:.4f}, Macro-F1={f1_raw:.4f}")

cm_raw = confusion_matrix(yte, pred_raw, labels=sorted(np.unique(y)))
disp = ConfusionMatrixDisplay(cm_raw, display_labels=sorted(np.unique(y)))
plt.figure(figsize=(5.2,4.6))
disp.plot(values_format='d', cmap="Blues", colorbar=False)
plt.title("混淆矩阵 - RF（原始特征）")
plt.tight_layout(); plt.savefig("CM_RF_原始特征.png"); plt.show()

# 随机森林（PCA特征）
rf_pca = RandomForestClassifier(n_estimators=400, max_depth=None, random_state=RANDOM_STATE, n_jobs=-1, class_weight="balanced")
rf_pca.fit(Xtr_pca, ytr)
pred_pca = rf_pca.predict(Xte_pca)
print("【RF-PCA特征】")
print(classification_report(yte, pred_pca, digits=4))
acc_pca = accuracy_score(yte, pred_pca); f1_pca = f1_score(yte, pred_pca, average="macro")
print(f"Accuracy={acc_pca:.4f}, Macro-F1={f1_pca:.4f}")

cm_pca = confusion_matrix(yte, pred_pca, labels=sorted(np.unique(y)))
disp = ConfusionMatrixDisplay(cm_pca, display_labels=sorted(np.unique(y)))
plt.figure(figsize=(5.2,4.6))
disp.plot(values_format='d', cmap="Greens", colorbar=False)
plt.title("混淆矩阵 - RF（PCA特征）")
plt.tight_layout(); plt.savefig("CM_RF_PCA特征.png"); plt.show()

perm = permutation_importance(rf_raw, Xte_raw, yte, n_repeats=10, random_state=RANDOM_STATE, n_jobs=-1)
imp_idx = np.argsort(perm.importances_mean)[::-1][:20]
plt.figure(figsize=(8.6,6))
plt.barh(np.array(feature_cols)[imp_idx][::-1], perm.importances_mean[imp_idx][::-1], xerr=perm.importances_std[imp_idx][::-1])
plt.xlabel("重要性（Permutation Mean ± STD）"); plt.title("Permutation Importance（原始手工特征，Top-20）")
plt.tight_layout(); plt.savefig("PermutationImportance_原始特征_Top20.png"); plt.show()

shap_sample = min(1500, len(Xtr_raw))
rs = np.random.RandomState(RANDOM_STATE)
idx_shap = rs.choice(len(Xtr_raw), shap_sample, replace=False)
Xtr_raw_small = Xtr_raw[idx_shap]
ytr_small = ytr[idx_shap]

explainer = shap.TreeExplainer(rf_raw)
shap_values = explainer.shap_values(Xtr_raw_small)  # list: per-class

explainer = shap.TreeExplainer(rf_raw)
shap_sample = min(1500, len(Xtr_raw))
rng = np.random.RandomState(42)
idx_shap = rng.choice(len(Xtr_raw), shap_sample, replace=False)
X_shap = Xtr_raw[idx_shap]     # 用的就是“原始手工特征流”的训练子集
y_shap = ytr[idx_shap]
shap_values_list = explainer.shap_values(X_shap)
def _align_shap_matrix(S, X):
    # S: (n_samples, nF或nF+1), X: (n_samples, nF)
    if S.shape[1] == X.shape[1]:
        return S
    if S.shape[1] == X.shape[1] + 1:
        return S[:, :-1]
    # 极少见：若仍不一致，取两者较小的公共宽度做保守对齐
    w = min(S.shape[1], X.shape[1])
    return S[:, :w], X[:, :w]

X_for_plot = X_shap
feat_names  = list(feature_cols)
aligned_sv_list = []
for c, Sv in enumerate(shap_values_list):
    if Sv.shape[1] == X_for_plot.shape[1]:
        aligned_sv_list.append(Sv)
    elif Sv.shape[1] == X_for_plot.shape[1] + 1:
        aligned_sv_list.append(Sv[:, :-1])
    else:
        # 极端兜底：取公共列数
        w = min(Sv.shape[1], X_for_plot.shape[1])
        aligned_sv_list.append(Sv[:, :w])
        X_for_plot = X_for_plot[:, :w]
        feat_names = feat_names[:w]

mean_abs_shap = np.mean(np.abs(np.stack(aligned_sv_list, axis=-1)), axis=(0,2))  # [n_features]
order = np.argsort(mean_abs_shap)[::-1][:25]
plt.figure(figsize=(9.2,6.2))
plt.barh(np.array(feat_names)[order][::-1], mean_abs_shap[order][::-1])
plt.xlabel("平均绝对SHAP值"); plt.title("全局特征重要性（SHAP，原始手工特征，Top-25）")
plt.tight_layout(); plt.savefig("SHAP_GlobalBar_Top25_fix.png"); plt.show()

pdp_features = list(np.array(feature_cols)[order[:6]])
fig, ax = plt.subplots(nrows=2, ncols=3, figsize=(12,6))
ax = ax.ravel()
for i, feat in enumerate(pdp_features):
    try:
        PartialDependenceDisplay.from_estimator(rf_raw, Xtr_raw, [feature_cols.index(feat)], ax=ax[i])
        ax[i].set_title(f"PDP：{feat}")
    except Exception as e:
        ax[i].set_visible(False)
plt.tight_layout(); plt.savefig("PDP_RF_原始特征_Top6.png"); plt.show()

key_feats_for_violin = pd.Index(feature_cols)[order[:6]].tolist()
sub = df_raw[["label"] + key_feats_for_violin].copy()
for feat in key_feats_for_violin:
    plt.figure(figsize=(7.8,4.6))
    # 用 pandas+matplotlib 画简易小提琴（不引入 seaborn）
    data_by_label = [sub[sub["label"]==lb][feat].values for lb in sorted(sub["label"].unique())]
    parts = plt.violinplot(data_by_label, showmeans=True, showmedians=False)
    for pc in parts['bodies']: pc.set_alpha(0.6)
    plt.xticks(ticks=range(1, 1+len(sorted(sub["label"].unique()))), labels=sorted(sub["label"].unique()))
    plt.xlabel("标签"); plt.ylabel(feat)
    plt.title(f"类内/类间分布对比 - {feat}")
    plt.tight_layout(); plt.savefig(f"Violin_{feat}.png"); plt.show()

corr_cols = feature_cols[:min(20, len(feature_cols))]
corr = pd.DataFrame(df_raw[corr_cols]).corr()
plt.figure(figsize=(9.2,7.6))
im = plt.imshow(corr, interpolation="nearest", aspect="auto", cmap="coolwarm")
plt.colorbar(im, fraction=0.046, pad=0.04)
plt.xticks(range(len(corr_cols)), corr_cols, rotation=60, ha="right", fontsize=9)
plt.yticks(range(len(corr_cols)), corr_cols, fontsize=9)
plt.title("手工特征相关性热力图（前20维）")
plt.tight_layout(); plt.savefig("特征相关性热力图.png"); plt.show()

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=RANDOM_STATE)
accs, f1s = [], []
for fold, (tr, te) in enumerate(skf.split(X_pca, y), 1):
    model = RandomForestClassifier(n_estimators=400, random_state=RANDOM_STATE, n_jobs=-1, class_weight="balanced")
    model.fit(X_pca[tr], y[tr])
    p = model.predict(X_pca[te])
    accs.append(accuracy_score(y[te], p))
    f1s.append(f1_score(y[te], p, average="macro"))
print("5折交叉验证（PCA特征 + RF）：")
print("Acc 平均/Std：", np.mean(accs).round(4), np.std(accs).round(4))
print("Macro-F1 平均/Std：", np.mean(f1s).round(4), np.std(f1s).round(4))

plt.figure(figsize=(7.5,3.6))
plt.plot(range(1,6), accs, marker="o", label="Acc")
plt.plot(range(1,6), f1s, marker="s", label="Macro-F1")
plt.xticks(range(1,6)); plt.ylim(0,1.0)
plt.xlabel("Fold"); plt.ylabel("Score"); plt.title("5-Fold 结果（PCA特征 + RF）")
plt.legend(); plt.tight_layout(); plt.savefig("CV5_RF_PCA.png"); plt.show()

# CELL 1
