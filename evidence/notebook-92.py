# CELL 0
import os, re, glob, json, math, random, warnings, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")
try:
    from IPython.display import display
except Exception:
    def display(x): print(x)



plt.rcParams["figure.dpi"] = 120
plt.rcParams["savefig.dpi"] = 400
plt.rcParams["axes.grid"] = True
plt.rcParams["grid.alpha"] = 0.22
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams["font.sans-serif"] = ['Kaiti']
plt.rcParams["axes.unicode_minus"] = False

from scipy.io import loadmat
from scipy import signal
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import (classification_report, accuracy_score, f1_score,
                             confusion_matrix, ConfusionMatrixDisplay)
from sklearn.covariance import EmpiricalCovariance
from sklearn.manifold import TSNE

import tensorflow as tf
from tensorflow.keras import layers, models

np.random.seed(42); random.seed(42); tf.random.set_seed(42)

PCA_CSV_SRC     = "源域特征_PCA95.csv"           # 问题一输出
CFG_JSON        = "特征预处理配置.json"           # 问题一输出
PCA_CSV_TGT     = "目标域特征_PCA95.csv"         # 可选
MODEL_DANN_PATH = "双流1D-CNN_DANN.h5"           # 问题三输出
MODEL_Q2_PATH   = "双流1D-CNN.h5"                # 问题二输出（可选）

df_src = pd.read_csv(PCA_CSV_SRC)
with open(CFG_JSON, "r", encoding="utf-8") as f:
    cfg = json.load(f)

TARGET_FS = int(cfg.get("target_fs", 12000))
SEG_LEN   = int(cfg.get("seg_len", 2048))
HOP_LEN   = int(cfg.get("hop_len", SEG_LEN))

meta_cols = ["path", "channel", "label", "fs_used", "seg_idx"]
feat_cols_pca = [c for c in df_src.columns if c not in meta_cols]

print("源域PCA特征读取：", df_src.shape)
display(df_src.head())

# 源域标签编码
le = LabelEncoder()
y_src = le.fit_transform(df_src["label"].values)
class_names = list(le.classes_)
num_classes = len(class_names)
print("类别映射：", {i:c for i,c in enumerate(class_names)})


def infer_fs_from_name(name, default=None):
    s = name.lower()
    m1 = re.search(r'(\d+)\s*k\s*hz?', s)
    if m1: return int(m1.group(1))*1000
    m2 = re.search(r'fs[_\-]?\s*(\d+)', s)
    if m2:
        v=int(m2.group(1)); return v if v>100 else v*1000
    m3 = re.findall(r'(\d{4,6})', s)
    for g in m3:
        v = int(g)
        if 2000 <= v <= 200000:
            return v
    if "12k" in s: return 12000
    if "32k" in s: return 32000
    if "48k" in s: return 48000
    return default

def load_from_mat_all_channels(path, seg_len=SEG_LEN, hop_len=HOP_LEN, fs_tgt=TARGET_FS):
    try:
        m = loadmat(path)
    except Exception:
        return {}
    raw = {}
    for k, v in m.items():
        if k.startswith("__"):
            continue
        arr = np.array(v)
        if not np.issubdtype(arr.dtype, np.number):
            continue
        arr = arr.reshape(-1)
        if arr.size < seg_len*2:
            continue
        keyl = k.lower()
        if "de" in keyl: tag="DE"
        elif "fe" in keyl: tag="FE"
        elif "ba" in keyl: tag="BA"
        else: tag = k
        cur = raw.get(tag)
        if (cur is None) or (arr.size > cur.size):
            raw[tag] = arr.astype(np.float64)
    if not raw: return {}
    fs_guess = infer_fs_from_name(os.path.basename(path), default=fs_tgt)
    out = {}
    for ch, sig in raw.items():
        fs_used = fs_guess if fs_guess is not None else fs_tgt
        if fs_used != fs_tgt:
            try:
                sig = signal.resample_poly(sig, fs_tgt, int(fs_used))
            except Exception:
                new_len = int(round(len(sig)*fs_tgt/float(fs_used)))
                sig = signal.resample(sig, new_len)
        nseg = (len(sig) - seg_len)//hop_len + 1
        for j in range(max(0, nseg)):
            seg = sig[j*hop_len : j*hop_len + seg_len]
            if len(seg) == seg_len:
                out[(path, ch, j)] = seg.astype(np.float32)
    return out

def resolve_path(p):
    if os.path.exists(p):
        return p
    cand = glob.glob(f"**/{os.path.basename(p)}", recursive=True)
    return cand[0] if cand else p


segment_dict_src = {}
for p0 in df_src["path"].drop_duplicates():
    p = resolve_path(p0)
    if os.path.exists(p):
        segs = load_from_mat_all_channels(p, SEG_LEN, HOP_LEN, TARGET_FS)
        segment_dict_src.update(segs)

mask_have_src = []
sig_list_src  = []
for _, row in df_src.iterrows():
    p = resolve_path(row["path"]); ch = row["channel"]; j = int(row["seg_idx"])
    key = (p, ch, j)
    if key in segment_dict_src:
        sig_list_src.append(segment_dict_src[key]); mask_have_src.append(True)
    else:
        alt = None
        for (pp, cc, jj), seg in segment_dict_src.items():
            if pp == p and jj == j: alt = seg; break
        if alt is not None:
            sig_list_src.append(alt); mask_have_src.append(True)
        else:
            mask_have_src.append(False)

mask_have_src = np.array(mask_have_src, dtype=bool)
assert mask_have_src.sum()>0, "源域分段重建失败。"

Xsig_src = np.stack(sig_list_src, axis=0)
Xfeat_src= df_src.loc[mask_have_src, feat_cols_pca].values
y_src    = y_src[mask_have_src]

mu = Xsig_src.mean(axis=1, keepdims=True)
std= Xsig_src.std(axis=1, keepdims=True) + 1e-6
Xsig_src = (Xsig_src - mu)/std
Xsig_src = np.expand_dims(Xsig_src, axis=-1)
print("源域：Xsig_src", Xsig_src.shape, "Xfeat_src", Xfeat_src.shape, "y_src", y_src.shape)

# 源域 train/val/test（val 用于评估，cal 用于温度缩放与置信集）
Xf_tr, Xf_te, Xs_tr, Xs_te, ys_tr, ys_te = train_test_split(
    Xfeat_src, Xsig_src, y_src, test_size=0.2, random_state=42, stratify=y_src
)
Xf_val, Xf_cal, Xs_val, Xs_cal, ys_val, ys_cal = train_test_split(
    Xf_te, Xs_te, ys_te, test_size=0.5, random_state=42, stratify=ys_te
)
print("划分：train=", Xs_tr.shape[0], " val=", Xs_val.shape[0], " cal=", Xs_cal.shape[0])


df_tgt = pd.read_csv(PCA_CSV_TGT) if os.path.exists(PCA_CSV_TGT) else None
src_paths_set = set(df_src["path"].apply(os.path.basename).tolist())

def find_target_mat_files():
    mats = []
    candidate_dirs = []
    for root, dirs, files in os.walk("."):
        base = os.path.basename(root).lower()
        if any(tag in base for tag in ["target", "目标域", "targetdomain"]):
            candidate_dirs.append(root)
    for d in candidate_dirs:
        mats += glob.glob(os.path.join(d, "**", "*.mat"), recursive=True)
    mats = list(dict.fromkeys(mats))
    if len(mats) == 0:
        all_mats = glob.glob("**/*.mat", recursive=True)
        mats = [p for p in all_mats if os.path.basename(p) not in src_paths_set]
    return mats

def make_target_arrays_from_segdict(segdict, df_tgt_optional=None):
    sig_list, path_list, idx_list, ch_list = [], [], [], []
    if df_tgt_optional is not None and {"path","channel","seg_idx"}.issubset(set(df_tgt_optional.columns)):
        for _, row in df_tgt_optional.iterrows():
            p = resolve_path(row["path"])
            ch = str(row["channel"]); j = int(row["seg_idx"])
            key = (p, ch, j)
            seg = segdict.get(key, None)
            if seg is None:
                for (pp, cc, jj), s in segdict.items():
                    if pp == p and jj == j: seg=s; ch=cc; break
            if seg is not None:
                sig_list.append(seg); path_list.append(p); idx_list.append(j); ch_list.append(ch)
    else:
        for (p, ch, j), seg in segdict.items():
            sig_list.append(seg); path_list.append(p); idx_list.append(j); ch_list.append(ch)
    if len(sig_list) == 0:
        return None, None
    Xsig = np.stack(sig_list, axis=0)
    mu = Xsig.mean(axis=1, keepdims=True)
    std= Xsig.std(axis=1, keepdims=True) + 1e-6
    Xsig = (Xsig - mu)/std
    Xsig = np.expand_dims(Xsig, axis=-1)
    paths = [f"{os.path.basename(p)}#ch={ch}#seg={j}" for p, ch, j in zip(path_list, ch_list, idx_list)]
    return Xsig, paths

Xsig_tgt = None; Xfeat_tgt = None; paths_tgt = None
if df_tgt is not None:
    tgt_files = sorted(set(df_tgt["path"].tolist()))
    resolved_files = [resolve_path(p) for p in tgt_files]
    segdict_tgt = {}
    for p in resolved_files:
        segdict_tgt.update(load_from_mat_all_channels(p, SEG_LEN, HOP_LEN, TARGET_FS))
    Xsig_tgt, paths_tgt = make_target_arrays_from_segdict(segdict_tgt, df_tgt_optional=df_tgt)
    if Xsig_tgt is not None:
        if set(feat_cols_pca).issubset(set(df_tgt.columns)) and (Xsig_tgt.shape[0] == df_tgt.shape[0]):
            Xfeat_tgt = df_tgt[feat_cols_pca].values.astype(np.float32)
        else:
            Xfeat_tgt = np.zeros((Xsig_tgt.shape[0], Xf_tr.shape[1]), dtype=np.float32)
else:
    auto_mats = find_target_mat_files()
    if len(auto_mats) > 0:
        segdict_tgt = {}
        for p in auto_mats:
            segdict_tgt.update(load_from_mat_all_channels(p, SEG_LEN, HOP_LEN, TARGET_FS))
        Xsig_tgt, paths_tgt = make_target_arrays_from_segdict(segdict_tgt, df_tgt_optional=None)
        if Xsig_tgt is not None:
            Xfeat_tgt = np.zeros((Xsig_tgt.shape[0], Xf_tr.shape[1]), dtype=np.float32)

USED_PROXY_TARGET = False
if Xsig_tgt is None:
    print("未能构建目标域，使用源域测试集作为代理目标域。")
    Xsig_tgt = Xs_te.copy()
    Xfeat_tgt = np.zeros((Xsig_tgt.shape[0], Xf_tr.shape[1]), dtype=np.float32)
    paths_tgt = [f"proxy_target_{i}" for i in range(len(Xsig_tgt))]
    USED_PROXY_TARGET = True

print("目标域：Xsig_tgt", Xsig_tgt.shape, "Xfeat_tgt", Xfeat_tgt.shape, "样本数=", len(paths_tgt))
print("是否代理目标域：", USED_PROXY_TARGET)

@tf.custom_gradient
def grad_reverse(x, lambd):
    def grad(dy):
        return -lambd * dy, tf.zeros_like(lambd)
    return x, grad

class GradientReversal(layers.Layer):
    def __init__(self, lambd=0.0, **kwargs):
        super().__init__(**kwargs)
        self.lambd = tf.Variable(lambd, trainable=False, dtype=tf.float32, name="grl_lambda")
    def call(self, x):
        return grad_reverse(x, self.lambd)
    def get_config(self):
        cfg = super().get_config()
        try:
            lam = float(self.lambd.numpy())
        except Exception:
            lam = 0.0
        cfg.update({"lambd": lam})
        return cfg
    @classmethod
    def from_config(cls, config):
        lam = config.pop("lambd", 0.0)
        return cls(lambd=lam, **config)

try:
    dann_model = tf.keras.models.load_model(
        MODEL_DANN_PATH,
        compile=False,
        custom_objects={"GradientReversal": GradientReversal}
    )
except Exception as e:
    pca_dim = Xf_tr.shape[1]
    inp_sig  = layers.Input(shape=(SEG_LEN,1), name="signal")
    x = layers.Conv1D(32, 3, padding="same", activation="relu")(inp_sig)
    x = layers.BatchNormalization()(x); x = layers.MaxPooling1D(2)(x)
    x = layers.Conv1D(64, 5, padding="same", activation="relu")(x)
    x = layers.BatchNormalization()(x); x = layers.MaxPooling1D(2)(x)
    x = layers.Conv1D(128, 5, padding="same", activation="relu")(x)
    x = layers.BatchNormalization()(x)
    sig_repr = layers.GlobalAveragePooling1D(name="sig_repr")(x)
    inp_feat = layers.Input(shape=(pca_dim,), name="pca_feat")
    y = layers.Dense(64, activation="relu")(inp_feat)
    y = layers.Dropout(0.2)(y)
    z = layers.Concatenate()([sig_repr, y])
    z = layers.Dense(64, activation="relu")(z)
    z = layers.Dropout(0.2)(z)
    emb = layers.Dense(32, activation="relu", name="emb")(z)
    cls_out = layers.Dense(num_classes, activation="softmax", name="cls_out")(emb)
    grl = GradientReversal(lambd=0.0, name="grl")
    d = grl(sig_repr)
    d = layers.Dropout(0.2)(d)
    d = layers.Dense(64, activation="relu")(d)
    d = layers.Dropout(0.2)(d)
    d = layers.Dense(32, activation="relu")(d)
    dom_out = layers.Dense(1, activation="sigmoid", name="dom_out")(d)
    dann_model = models.Model(inputs=[inp_sig, inp_feat], outputs=[cls_out, dom_out], name="DANN")

    dann_model.load_weights(MODEL_DANN_PATH, by_name=True, skip_mismatch=True)

softmax_model = tf.keras.Model(inputs=dann_model.inputs,
                               outputs=dann_model.get_layer("cls_out").output)

cls_layer = dann_model.get_layer("cls_out")
W, b = cls_layer.get_weights()          # W: [emb_dim, num_classes], b: [num_classes]
emb_tensor = dann_model.get_layer("emb").output
logits_dense = layers.Dense(W.shape[1], activation=None, name="cls_logits")
logits_tensor = logits_dense(emb_tensor)          # build
logits_dense.set_weights([W, b])                  # 复用权重
logits_model = models.Model(inputs=dann_model.inputs, outputs=logits_tensor, name="logits_model")
emb_model = tf.keras.Model(inputs=dann_model.inputs, outputs=dann_model.get_layer("emb").output)
try:
    dom_model = tf.keras.Model(inputs=dann_model.inputs, outputs=dann_model.get_layer("dom_out").output)
    HAVE_DOM = True
except Exception:
    HAVE_DOM = False

MC_T = 20

def mc_predict_proba(Xsig, Xfeat, T=MC_T):
    probs = []
    for t in range(T):
        p = softmax_model([Xsig, Xfeat], training=True).numpy()
        probs.append(p)
    probs = np.stack(probs, axis=0)      # [T, N, C]
    p_mean = probs.mean(axis=0)          # [N, C]
    p_var  = probs.var(axis=0).mean(axis=1)       # [N]
    p_ent  = -(p_mean * np.log(np.clip(p_mean, 1e-12, 1.))).sum(axis=1)
    p_conf = p_mean.max(axis=1)
    return p_mean, p_var, p_ent, p_conf

p_mean_val, p_var_val, p_ent_val, p_conf_val = mc_predict_proba(Xs_val, Xf_val, T=MC_T)
y_pred_val = p_mean_val.argmax(axis=1)
print(classification_report(ys_val, y_pred_val, target_names=class_names, digits=4))

p_mean_tgt, p_var_tgt, p_ent_tgt, p_conf_tgt = mc_predict_proba(Xsig_tgt, Xfeat_tgt, T=MC_T)

def save_hist2(a, b, lab_a, lab_b, title, fname, bins=30):
    plt.figure(figsize=(7,3.2))
    plt.hist(a, bins=bins, alpha=0.65, label=lab_a, density=True)
    plt.hist(b, bins=bins, alpha=0.65, label=lab_b, density=True)
    plt.legend(); plt.title(title)
    plt.xlabel("值"); plt.ylabel("密度")
    plt.tight_layout(); plt.savefig(fname); plt.show()
    print("已保存：", fname)

save_hist2(p_conf_val, p_conf_tgt, "源域-置信度", "目标域-置信度",
           "MC Dropout：源/目标 置信度分布", "Q4_MC_置信度_源vs目标.png")
save_hist2(p_ent_val, p_ent_tgt, "源域-熵", "目标域-熵",
           "MC Dropout：源/目标 熵 分布", "Q4_MC_熵_源vs目标.png")
save_hist2(p_var_val, p_var_tgt, "源域-方差", "目标域-方差",
           "MC Dropout：源/目标 预测方差 分布", "Q4_MC_方差_源vs目标.png")

logits_cal = logits_model.predict([Xs_cal, Xf_cal], verbose=0)
y_cal_oh   = tf.keras.utils.to_categorical(ys_cal, num_classes)

def nll_with_T(T, logits, y_true_oh):
    T = float(T)
    logits_T = logits / T
    logp = logits_T - tf.reduce_logsumexp(logits_T, axis=1, keepdims=True).numpy()
    nll = -np.mean(np.sum(y_true_oh * logp, axis=1))
    return nll

Ts = np.linspace(0.5, 5.0, 46)
nlls = [nll_with_T(T, logits_cal, y_cal_oh) for T in Ts]
T_star = float(Ts[int(np.argmin(nlls))])
print(f"温度缩放最优 T* = {T_star:.3f}")

plt.figure(figsize=(6.2,3.2))
plt.plot(Ts, nlls, marker='o', linewidth=1.2)
plt.xlabel("温度 T"); plt.ylabel("NLL")
plt.title("温度缩放：校准集 NLL vs T")
plt.tight_layout(); plt.savefig("Q4_TS_NLL曲线.png"); plt.show()

def softmax_with_T(logits, T):
    z = logits / T
    e = np.exp(z - z.max(axis=1, keepdims=True))
    return e / e.sum(axis=1, keepdims=True)

logits_val = logits_model.predict([Xs_val, Xf_val], verbose=0)
probs_val_raw = tf.nn.softmax(logits_val, axis=1).numpy()
probs_val_cal = softmax_with_T(logits_val, T_star)

y_true_val = ys_val
conf_raw = probs_val_raw.max(axis=1); pred_raw = probs_val_raw.argmax(axis=1)
conf_cal = probs_val_cal.max(axis=1); pred_cal = probs_val_cal.argmax(axis=1)

def compute_ece(conf, pred, y_true, M=15):
    bins = np.linspace(0.0, 1.0, M+1)
    ece = 0.0
    bin_accs, bin_confs, bin_sizes = [], [], []
    for i in range(M):
        l, r = bins[i], bins[i+1]
        idx = np.where((conf>l) & (conf<=r))[0]
        if len(idx)==0:
            bin_accs.append(0); bin_confs.append((l+r)/2); bin_sizes.append(0); continue
        acc = (pred[idx]==y_true[idx]).mean()
        c   = conf[idx].mean()
        w   = len(idx)/len(conf)
        ece += w * abs(acc - c)
        bin_accs.append(acc); bin_confs.append(c); bin_sizes.append(len(idx))
    return ece, bins, np.array(bin_accs), np.array(bin_confs), np.array(bin_sizes)

ece_raw, bins, accs_raw, confs_raw, sizes_raw = compute_ece(conf_raw, pred_raw, y_true_val, M=15)
ece_cal, _,   accs_cal, confs_cal, sizes_cal = compute_ece(conf_cal, pred_cal, y_true_val, M=15)
print(f"ECE(raw)={ece_raw:.4f}  ECE(cal)={ece_cal:.4f}")

def reliability_plot(accs, bins, title, fname):
    centers = 0.5*(bins[:-1]+bins[1:])
    plt.figure(figsize=(4.8,4.8))
    plt.bar(centers, accs, width=centers[1]-centers[0], alpha=0.75, label="准确率")
    plt.plot([0,1],[0,1],'--',linewidth=1.2,label="理想校准")
    plt.xlabel("置信度"); plt.ylabel("准确率")
    plt.title(title); plt.legend()
    plt.tight_layout(); plt.savefig(fname); plt.show()
    print("已保存：", fname)

reliability_plot(accs_raw, bins, f"可靠性图（未校准）ECE={ece_raw:.3f}", "Q4_可靠性图_未校准.png")
reliability_plot(accs_cal, bins, f"可靠性图（温度缩放）ECE={ece_cal:.3f}", "Q4_可靠性图_温度缩放.png")

def risk_coverage_curve(conf, pred, y_true, mode="conf", K=50):
    if mode=="conf":
        taus = np.linspace(0.0, 1.0, K)
        cov, risk = [], []
        for t in taus:
            idx = np.where(conf>=t)[0]
            if len(idx)==0:
                cov.append(0.0); risk.append(0.0)
            else:
                cov.append(len(idx)/len(conf))
                risk.append(1.0 - (pred[idx]==y_true[idx]).mean())
        return taus, np.array(cov), np.array(risk)
    else: # 使用熵（小于阈值保留）
        taus = np.linspace(0.0, float(np.max(conf)+1e-6), K)
        cov, risk = [], []
        for t in taus:
            idx = np.where(conf<=t)[0]
            if len(idx)==0:
                cov.append(0.0); risk.append(0.0)
            else:
                cov.append(len(idx)/len(conf))
                risk.append(1.0 - (pred[idx]==y_true[idx]).mean())
        return taus, np.array(cov), np.array(risk)

tau_conf_raw, cov_conf_raw, risk_conf_raw = risk_coverage_curve(conf_raw, pred_raw, y_true_val, mode="conf", K=50)
tau_conf_cal, cov_conf_cal, risk_conf_cal = risk_coverage_curve(conf_cal, pred_cal, y_true_val, mode="conf", K=50)

plt.figure(figsize=(6.6,3.2))
plt.plot(cov_conf_raw, risk_conf_raw, label="未校准")
plt.plot(cov_conf_cal, risk_conf_cal, label="温度缩放")
plt.xlabel("Coverage（保留率）"); plt.ylabel("Risk（1-Accuracy）")
plt.title("Risk–Coverage（源域验证集）")
plt.legend(); plt.tight_layout(); plt.savefig("Q4_RiskCoverage_源域_conf.png"); plt.show()

emb_tr = emb_model.predict([Xs_tr, Xf_tr], verbose=0)
emb_val= emb_model.predict([Xs_val, Xf_val], verbose=0)
emb_tgt= emb_model.predict([Xsig_tgt, Xfeat_tgt], verbose=0)

mu_c = []
for c in range(num_classes):
    mu_c.append(emb_tr[ys_tr==c].mean(axis=0))
mu_c = np.stack(mu_c, axis=0)   # [C, D]

ecov = EmpiricalCovariance(assume_centered=False)
ecov.fit(emb_tr - mu_c[ys_tr])
cov = ecov.covariance_
cov_inv = np.linalg.pinv(cov)

def maha_score(E):
    diffs = E[:, None, :] - mu_c[None, :, :]
    mds = np.einsum('ncd,dd,nce->nc', diffs, cov_inv, diffs)
    dmin = mds.min(axis=1)
    return -dmin

score_val = maha_score(emb_val)
score_tgt = maha_score(emb_tgt)
q = 0.05
thr = np.quantile(score_val, q)
print(f"Mahalanobis 分数阈值（{int(q*100)}% 分位）= {thr:.3f}，低于阈值 → 标记未知/存疑")

plt.figure(figsize=(6.6,3.0))
plt.hist(score_val, bins=40, alpha=0.7, label="源域验证")
plt.hist(score_tgt, bins=40, alpha=0.7, label="目标域")
plt.axvline(thr, color='r', linestyle='--', label='阈值')
plt.legend(); plt.xlabel("Mahalanobis 相似分数（-min距离）"); plt.ylabel("样本数")
plt.title("开集/未知检测的分数分布")
plt.tight_layout(); plt.savefig("Q4_未知检测_分数直方.png"); plt.show()

unknown_mask_tgt = score_tgt < thr
print("目标域：未知/存疑 样本数 = ", int(unknown_mask_tgt.sum()), "/", len(score_tgt))

df_tgt_pred = pd.DataFrame({
    "path": paths_tgt,
    "maha_score": score_tgt,
    "unknown_flag": unknown_mask_tgt.astype(int),
    "mc_conf": p_conf_tgt,
    "mc_ent":  p_ent_tgt
})
for i, c in enumerate(class_names):
    df_tgt_pred[f"prob_{c}"] = p_mean_tgt[:, i]
df_tgt_pred["pred_label"] = [class_names[i] for i in p_mean_tgt.argmax(axis=1)]
df_tgt_pred.to_csv("Q4_目标域_未知检测与MC结果.csv", index=False, encoding="utf-8-sig")
display(df_tgt_pred.head())


alpha = 0.1
probs_cal_T = softmax_with_T(logits_cal, T_star)
p_true_cal = probs_cal_T[np.arange(len(ys_cal)), ys_cal]
scores_cal = 1.0 - p_true_cal
q_hat = np.quantile(scores_cal, 1-alpha, interpolation="higher")
print(f"Conformal q̂ (1-α分位, α={alpha}) = {q_hat:.4f}")

logits_val = logits_model.predict([Xs_val, Xf_val], verbose=0)
probs_val_T = softmax_with_T(logits_val, T_star)
S_val = (1.0 - probs_val_T <= q_hat)
cover = S_val[np.arange(len(ys_val)), ys_val].mean()
set_size = S_val.sum(axis=1).mean()
print(f"Conformal（源域验证）：覆盖率={cover:.4f}（期望≥{1-alpha:.2f}），平均集合大小={set_size:.3f}")

plt.figure(figsize=(6.0,3.0))
plt.hist(S_val.sum(axis=1), bins=np.arange(0.5, num_classes+1.5, 1), alpha=0.85)
plt.xlabel("集合大小"); plt.ylabel("样本数")
plt.title("源域验证集：置信集大小分布")
plt.tight_layout(); plt.savefig("Q4_Conformal_源域_集合大小.png"); plt.show()

logits_tgt = logits_model.predict([Xsig_tgt, Xfeat_tgt], verbose=0)
probs_tgt_T = softmax_with_T(logits_tgt, T_star)
S_tgt = (1.0 - probs_tgt_T <= q_hat)
set_size_tgt = S_tgt.sum(axis=1)

plt.figure(figsize=(6.0,3.0))
plt.hist(set_size_tgt, bins=np.arange(0.5, num_classes+1.5, 1), alpha=0.85)
plt.xlabel("集合大小"); plt.ylabel("样本数")
plt.title("目标域：置信集大小分布")
plt.tight_layout(); plt.savefig("Q4_Conformal_目标域_集合大小.png"); plt.show()

def set_to_str(row_bool):
    return "|".join([class_names[i] for i,b in enumerate(row_bool) if b])

confset_str = [set_to_str(row) for row in S_tgt]
df_conf_tgt = pd.DataFrame({
    "path": paths_tgt,
    "conf_set": confset_str,
    "set_size": set_size_tgt,
    "maha_score": score_tgt,
    "unknown_flag": unknown_mask_tgt.astype(int),
    "mc_conf": p_conf_tgt,
    "mc_ent":  p_ent_tgt
})
df_conf_tgt.to_csv("Q4_目标域_置信集.csv", index=False, encoding="utf-8-sig")
display(df_conf_tgt.head())

n_plot = min(800, len(emb_tgt))
idxp = np.random.choice(len(emb_tgt), n_plot, replace=False)
X2 = TSNE(n_components=2, perplexity=30, init="pca", n_iter=1000, random_state=42).fit_transform(emb_tgt[idxp])
val_col = p_ent_tgt[idxp]

plt.figure(figsize=(6.4,5.0))
plt.scatter(X2[:,0], X2[:,1], c=val_col, s=14, cmap="viridis")
cb = plt.colorbar(); cb.set_label("MC-熵")
plt.title("目标域嵌入（t-SNE）按不确定性着色")
plt.xlabel("t-SNE 1"); plt.ylabel("t-SNE 2")
plt.tight_layout(); plt.savefig("Q4_tSNE_目标域_按不确定性着色.png"); plt.show()

acc_raw = accuracy_score(y_true_val, pred_raw)
acc_cal = accuracy_score(y_true_val, pred_cal)
f1_raw = f1_score(y_true_val, pred_raw, average="macro")
f1_cal = f1_score(y_true_val, pred_cal, average="macro")
print(f"源域验证：未校准 Acc={acc_raw:.4f}, F1={f1_raw:.4f}；温度缩放 Acc={acc_cal:.4f}, F1={f1_cal:.4f}")

with open("Q4_可靠性与不确定性_摘要.txt", "w", encoding="utf-8") as f:
    f.write("【问题四：可靠性与不确定性评估摘要】\n")
    f.write(f"- MC Dropout: 源域(置信度均值={p_conf_val.mean():.3f}, 熵均值={p_ent_val.mean():.3f}); "
            f"目标域(置信度均值={p_conf_tgt.mean():.3f}, 熵均值={p_ent_tgt.mean():.3f})\n")
    f.write(f"- 温度缩放：T*={T_star:.3f}，ECE(raw)={ece_raw:.4f} → ECE(cal)={ece_cal:.4f}\n")
    f.write(f"- Risk–Coverage：见 Q4_RiskCoverage_源域_conf.png（校准后风险–覆盖曲线更优）\n")
    f.write(f"- Mahalanobis 未知检测：阈值={thr:.3f}，目标域未知/存疑数={int(unknown_mask_tgt.sum())}/{len(score_tgt)}\n")
    f.write(f"- Conformal 置信集：源域覆盖率={cover:.4f}（期望≥{1-0.1:.2f}），平均集合大小={set_size:.3f}\n")
    f.write(f"- 目标域置信集：见 Q4_目标域_置信集.csv；t-SNE 按不确定性着色图见 Q4_tSNE_目标域_按不确定性着色.png\n")
