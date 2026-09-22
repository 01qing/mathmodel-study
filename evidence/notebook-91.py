# CELL 0
import os, re, glob, json, math, random, warnings, time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")
from IPython.display import display



plt.rcParams["figure.dpi"] = 120
plt.rcParams["savefig.dpi"] = 220
plt.rcParams["axes.grid"] = True
plt.rcParams["grid.alpha"] = 0.22
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams["font.sans-serif"] = ['Kaiti']
plt.rcParams["axes.unicode_minus"] = False

from scipy.io import loadmat
from scipy import signal
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.manifold import TSNE
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay, accuracy_score, f1_score

import tensorflow as tf
from tensorflow.keras import layers, models, optimizers

np.random.seed(42); random.seed(42); tf.random.set_seed(42)

PCA_CSV_SRC   = "源域特征_PCA95.csv"         # 问题一输出
CFG_JSON      = "特征预处理配置.json"         # 问题一输出
MODEL_Q2_PATH = "双流_ResSE_Focal.h5"              # 问题二输出
PCA_CSV_TGT   = "目标域特征_PCA95.csv"

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

# 标签编码（源域）
le = LabelEncoder()
y_src = le.fit_transform(df_src["label"].values)
class_names = list(le.classes_)
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
    """
    加载 .mat 文件中的所有可用数值向量通道：
      * 优先识别含 'DE','FE','BA' 的键；否则保留所有长度足够的数值变量（作为通道名）。
      * 重采样到 fs_tgt；按非重叠切段；返回 {(path, ch, j): seg} 字典。
    """
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
        tag = None
        if "de" in keyl: tag="DE"
        elif "fe" in keyl: tag="FE"
        elif "ba" in keyl: tag="BA"
        else:
            tag = k  # 使用原变量名作为通道名
        cur = raw.get(tag)
        if (cur is None) or (arr.size > cur.size):
            raw[tag] = arr.astype(np.float64)

    if not raw:
        return {}

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
        for j in range(max(0,nseg)):
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
    p = resolve_path(row["path"])
    ch = row["channel"]; j = int(row["seg_idx"])
    key = (p, ch, j)
    if key in segment_dict_src:
        sig_list_src.append(segment_dict_src[key])
        mask_have_src.append(True)
    else:
        # 容错：同文件其他通道的同 j
        alt = None
        for (pp, cc, jj), seg in segment_dict_src.items():
            if pp == p and jj == j:
                alt = seg; break
        if alt is not None:
            sig_list_src.append(alt)
            mask_have_src.append(True)
        else:
            mask_have_src.append(False)

mask_have_src = np.array(mask_have_src, dtype=bool)

Xsig_src = np.stack(sig_list_src, axis=0)                  # [Ns, 2048]
Xfeat_src= df_src.loc[mask_have_src, feat_cols_pca].values # [Ns, K]
y_src    = y_src[mask_have_src]

mu = Xsig_src.mean(axis=1, keepdims=True)
std= Xsig_src.std(axis=1, keepdims=True) + 1e-6
Xsig_src = (Xsig_src - mu)/std
Xsig_src = np.expand_dims(Xsig_src, axis=-1)               # [Ns, 2048, 1]
print("源域：Xsig_src", Xsig_src.shape, "Xfeat_src", Xfeat_src.shape, "y_src", y_src.shape)

src_feat_mu = Xfeat_src.mean(axis=0)
src_feat_std= Xfeat_src.std(axis=0) + 1e-6
def sample_like_source(n_rows, mu, std):
    return mu + np.random.randn(n_rows, mu.shape[0]).astype(np.float32) * std

df_tgt = pd.read_csv(PCA_CSV_TGT) if os.path.exists(PCA_CSV_TGT) else None
src_paths_set = set(df_src["path"].apply(os.path.basename).tolist())
USED_PROXY_TARGET = False

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

def build_target_segments_from_mats(mat_files):
    segdict = {}
    for p in mat_files:
        p2 = resolve_path(p)
        try:
            segs = load_from_mat_all_channels(p2, SEG_LEN, HOP_LEN, TARGET_FS)
            segdict.update(segs)
        except Exception:
            pass
    return segdict

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
                    if pp == p and jj == j:
                        seg = s; ch = cc; break
            if seg is not None:
                sig_list.append(seg); path_list.append(p); idx_list.append(j); ch_list.append(ch)
    else:
        for (p, ch, j), seg in segdict.items():
            sig_list.append(seg); path_list.append(p); idx_list.append(j); ch_list.append(ch)

    if len(sig_list) == 0:
        return None, None, None, None

    Xsig = np.stack(sig_list, axis=0)
    mu = Xsig.mean(axis=1, keepdims=True)
    std= Xsig.std(axis=1, keepdims=True) + 1e-6
    Xsig = (Xsig - mu)/std
    Xsig = np.expand_dims(Xsig, axis=-1)
    paths = [f"{os.path.basename(p)}#ch={ch}#seg={j}" for p, ch, j in zip(path_list, ch_list, idx_list)]
    return Xsig, paths, np.array(idx_list), np.array(ch_list)

# 目标域张量
Xsig_tgt = None; Xfeat_tgt = None; paths_tgt = None
need_placeholder_for_target_features = False

if df_tgt is not None:
    tgt_files = sorted(set(df_tgt["path"].tolist()))
    resolved_files = [resolve_path(p) for p in tgt_files]
    segdict_tgt = build_target_segments_from_mats(resolved_files)
    Xsig_tgt, paths_tgt, idxs_tgt, chs_tgt = make_target_arrays_from_segdict(segdict_tgt, df_tgt_optional=df_tgt)
    if Xsig_tgt is not None:
        if set(feat_cols_pca).issubset(set(df_tgt.columns)) and (Xsig_tgt.shape[0] == df_tgt.shape[0]):
            Xfeat_tgt = df_tgt[feat_cols_pca].values.astype(np.float32)
        else:
            need_placeholder_for_target_features = True
else:
    auto_mats = find_target_mat_files()
    if len(auto_mats) > 0:
        segdict_tgt = build_target_segments_from_mats(auto_mats)
        Xsig_tgt, paths_tgt, idxs_tgt, chs_tgt = make_target_arrays_from_segdict(segdict_tgt, df_tgt_optional=None)
        if Xsig_tgt is not None:
            need_placeholder_for_target_features = True

# 源域划分（供评估与“代理目标域”回退）
Xf_tr, Xf_te, Xs_tr, Xs_te, ys_tr, ys_te = train_test_split(
    Xfeat_src, Xsig_src, y_src, test_size=0.2, random_state=42, stratify=y_src
)

if Xsig_tgt is None:
    print("未能有效构建‘目标域’，使用源域测试集作为‘代理目标域’（无标签参与训练）。")
    Xsig_tgt = Xs_te.copy()
    Xfeat_tgt = sample_like_source(Xsig_tgt.shape[0], src_feat_mu, src_feat_std)
    paths_tgt = [f"proxy_target_{i}" for i in range(len(Xsig_tgt))]
    USED_PROXY_TARGET = True
else:
    USED_PROXY_TARGET = False
    if need_placeholder_for_target_features:
        Xfeat_tgt = sample_like_source(Xsig_tgt.shape[0], src_feat_mu, src_feat_std)

print("目标域：Xsig_tgt", Xsig_tgt.shape, "Xfeat_tgt", Xfeat_tgt.shape, "样本数=", len(paths_tgt))
print("是否为代理目标域：", USED_PROXY_TARGET)

num_classes = len(class_names)
pca_dim = Xf_tr.shape[1]

inp_sig  = layers.Input(shape=(SEG_LEN,1), name="signal")
x = layers.Conv1D(32, 3, padding="same", activation="relu")(inp_sig)
x = layers.BatchNormalization()(x); x = layers.MaxPooling1D(2)(x)
x = layers.Conv1D(64, 5, padding="same", activation="relu")(x)
x = layers.BatchNormalization()(x); x = layers.MaxPooling1D(2)(x)
x = layers.Conv1D(128, 5, padding="same", activation="relu")(x)
x = layers.BatchNormalization()(x)
sig_repr = layers.GlobalAveragePooling1D(name="sig_repr")(x)   # <— 信号流 GAP 表征

inp_feat= layers.Input(shape=(pca_dim,), name="pca_feat")
y = layers.Dense(64, activation="relu")(inp_feat)
y = layers.Dropout(0.2)(y)

z = layers.Concatenate()([sig_repr, y])
z = layers.Dense(64, activation="relu")(z)
z = layers.Dropout(0.2)(z)
emb = layers.Dense(32, activation="relu", name="emb")(z)

cls_out = layers.Dense(num_classes, activation="softmax", name="cls_out")(emb)
base_model = models.Model(inputs=[inp_sig, inp_feat], outputs=cls_out, name="base_dualstream")
base_model.load_weights(MODEL_Q2_PATH, by_name=True, skip_mismatch=True)

for lyr in base_model.layers:
    if isinstance(lyr, tf.keras.layers.BatchNormalization):
        lyr.trainable = False

SNAP_BEFORE = "BASELINE_BEFORE_DANN.weights.h5"
base_model.save_weights(SNAP_BEFORE)


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

grl = GradientReversal(lambd=0.0, name="grl")
d = grl(sig_repr)                                 # <— 仅看信号流表征
d = layers.Dropout(0.2)(d)
d = layers.Dense(64, activation="relu")(d)
d = layers.Dropout(0.2)(d)
d = layers.Dense(32, activation="relu")(d)
dom_out = layers.Dense(1, activation="sigmoid", name="dom_out")(d)

dann_model = models.Model(inputs=[inp_sig, inp_feat], outputs=[cls_out, dom_out], name="DANN")

for lyr in dann_model.layers:
    if isinstance(lyr, tf.keras.layers.BatchNormalization):
        lyr.trainable = False

opt = optimizers.Adam(learning_rate=1e-3, clipnorm=1.0)   # 轻度裁剪抑制过快饱和
bce = tf.keras.losses.BinaryCrossentropy()
cce = tf.keras.losses.CategoricalCrossentropy()

BATCH = 512
steps_per_epoch = int(math.ceil(max(len(Xs_tr), len(Xsig_tgt)) / BATCH))
EPOCHS = 16
lambda_max = 0.3                        # 适度增强对抗强度
ys_tr_oh = tf.keras.utils.to_categorical(ys_tr, num_classes)

def batch_iter(Xsig, Xfeat, Y, bs):
    n = len(Xsig)
    idx = np.arange(n); np.random.shuffle(idx)
    for i in range(0, n, bs):
        sel = idx[i:i+bs]
        yield Xsig[sel], Xfeat[sel], Y[sel]

def make_domain_labels(n_src, n_tgt):
    return np.concatenate([np.zeros((n_src,1), dtype=np.float32),
                           np.ones((n_tgt,1), dtype=np.float32)], axis=0)

hist_total, hist_cls_loss, hist_dom_loss, hist_dom_acc, hist_lambda = [], [], [], [], []

for epoch in range(1, EPOCHS+1):
    t0 = time.time()
    for step, (Xs_s, Xf_s, y_s) in enumerate(batch_iter(Xs_tr, Xf_tr, ys_tr_oh, BATCH)):
        # 目标域 batch（循环取样以对齐大小）
        i0 = (step*BATCH) % len(Xsig_tgt)
        i1 = min(i0+BATCH, len(Xsig_tgt))
        Xs_t = Xsig_tgt[i0:i1]
        Xf_t = Xfeat_tgt[i0:i1]
        if len(Xs_t) < len(Xs_s):
            left = len(Xs_s) - len(Xs_t)
            Xs_t = np.concatenate([Xs_t, Xsig_tgt[:left]], axis=0)
            Xf_t = np.concatenate([Xf_t, Xfeat_tgt[:left]], axis=0)

        # 拼接（源在前，目标在后）
        Xsig_b = np.concatenate([Xs_s, Xs_t], axis=0)
        Xfeat_b= np.concatenate([Xf_s, Xf_t], axis=0)
        y_dom_b= make_domain_labels(len(Xs_s), len(Xs_t))

        # Ganin 调度
        p = ((epoch-1)*steps_per_epoch + step) / (EPOCHS*steps_per_epoch)
        lamb = lambda_max * (2.0/(1.0+np.exp(-10.0*p)) - 1.0)
        dann_model.get_layer("grl").lambd.assign(lamb)

        with tf.GradientTape() as tape:
            y_pred_cls, y_pred_dom = dann_model([Xsig_b, Xfeat_b], training=True)
            # 分类损失：仅源域
            y_pred_cls_src = y_pred_cls[:len(Xs_s)]
            loss_cls = cce(y_s, y_pred_cls_src)
            # 域损失：源=0，目标=1
            loss_dom = bce(y_dom_b, y_pred_dom)
            loss_total = loss_cls + lamb * loss_dom

        grads = tape.gradient(loss_total, dann_model.trainable_variables)
        opt.apply_gradients(zip(grads, dann_model.trainable_variables))

        dom_acc = ((y_pred_dom.numpy()>0.5)==(y_dom_b>0.5)).astype(np.float32).mean()
        hist_total.append(loss_total.numpy())
        hist_cls_loss.append(loss_cls.numpy())
        hist_dom_loss.append(loss_dom.numpy())
        hist_dom_acc.append(dom_acc)
        hist_lambda.append(lamb)

    t1 = time.time()
    print(f"Epoch {epoch:02d}/{EPOCHS}  total={np.mean(hist_total[-steps_per_epoch:]):.4f} "
          f"cls={np.mean(hist_cls_loss[-steps_per_epoch:]):.4f} "
          f"dom={np.mean(hist_dom_loss[-steps_per_epoch:]):.4f} "
          f"dom_acc={np.mean(hist_dom_acc[-steps_per_epoch:]):.3f} "
          f"lambda={lamb:.3f}  ({t1-t0:.1f}s)")

def plot_curve(arr, title, fname, ylabel="值"):
    plt.figure(figsize=(7.6,3.4))
    plt.plot(arr, linewidth=1.2)
    plt.xlabel("Step"); plt.ylabel(ylabel); plt.title(title)
    plt.tight_layout(); plt.savefig(fname); plt.show()
    print("已保存：", fname)

plot_curve(hist_total,   "训练曲线：总损失 L = L_class + λ·L_domain", "DANN_总损失.png", "Loss")
plot_curve(hist_cls_loss,"训练曲线：分类损失 L_class（仅源域）",       "DANN_分类损失.png", "Loss")
plot_curve(hist_dom_loss,"训练曲线：域对齐损失 L_domain",           "DANN_域损失.png", "Loss")
plot_curve(hist_dom_acc, "训练曲线：域判别准确率",     "DANN_域准确率.png", "Accuracy")
plot_curve(hist_lambda,  "λ 调度（训练进程中的对抗强度）",            "DANN_λ调度.png", "λ")

# ----------------------------
# K. 源域测试集评估（分类） & 混淆矩阵
# ----------------------------
prob_src = dann_model.predict({"signal": Xs_te, "pca_feat": Xf_te}, verbose=0)[0]
pred_src = prob_src.argmax(axis=1)
print("\n【源域测试集（DANN 后）】")
print(classification_report(ys_te, pred_src, target_names=class_names, digits=4))
acc_src = accuracy_score(ys_te, pred_src); f1_src = f1_score(ys_te, pred_src, average="macro")
print(f"Acc={acc_src:.4f}, Macro-F1={f1_src:.4f}")

cm = confusion_matrix(ys_te, pred_src, labels=range(num_classes))
disp = ConfusionMatrixDisplay(cm, display_labels=class_names)
plt.figure(figsize=(5.4,4.8))
disp.plot(values_format='d', cmap="Greens", colorbar=False)
plt.title("混淆矩阵 - 源域测试集（DANN 后）")
plt.tight_layout(); plt.savefig("CM_源域_DANN.png"); plt.show()

# ----------------------------
# L. 目标域推断（无标签）：预测与置信度分析
# ----------------------------
prob_tgt = dann_model.predict({"signal": Xsig_tgt, "pca_feat": Xfeat_tgt}, verbose=0)[0]
pred_tgt = prob_tgt.argmax(axis=1)
conf_tgt = prob_tgt.max(axis=1)

plt.figure(figsize=(6.8,3.4))
plt.hist(conf_tgt, bins=20, alpha=0.85)
plt.xlabel("预测置信度（max Softmax）"); plt.ylabel("样本数")
plt.title("目标域样本置信度分布（DANN 后）")
plt.tight_layout(); plt.savefig("目标域_置信度分布.png"); plt.show()

plt.figure(figsize=(6.8,3.4))
vals, cnts = np.unique(pred_tgt, return_counts=True)
plt.bar([class_names[v] for v in vals], cnts)
plt.xlabel("预测类别"); plt.ylabel("样本数")
plt.title("目标域预测类别分布（DANN 后）")
plt.tight_layout(); plt.savefig("目标域_预测类别分布.png"); plt.show()

df_pred = pd.DataFrame({
    "path": paths_tgt,
    "pred_label": [class_names[i] for i in pred_tgt],
    "confidence": conf_tgt
})
for i, c in enumerate(class_names):
    df_pred[f"prob_{c}"] = prob_tgt[:, i]
df_pred.to_csv("目标域_预测结果.csv", index=False, encoding="utf-8-sig")
display(df_pred.head())

feat_model_after = tf.keras.Model(inputs=dann_model.inputs,
                                  outputs=dann_model.get_layer("emb").output)

base_model_before = tf.keras.models.clone_model(base_model)   # 独立层对象
base_model_before.load_weights(SNAP_BEFORE)                   # 载入训练前权重
feat_model_before = tf.keras.Model(inputs=base_model_before.inputs,
                                   outputs=base_model_before.get_layer("emb").output)

ns = min(800, len(Xs_te))
nt = min(800, len(Xsig_tgt))
idxs = np.random.choice(len(Xs_te), ns, replace=False)
idxt = np.random.choice(len(Xsig_tgt), nt, replace=False)

emb_src_before = feat_model_before.predict({"signal": Xs_te[idxs], "pca_feat": Xf_te[idxs]}, verbose=0)
emb_tgt_before = feat_model_before.predict({"signal": Xsig_tgt[idxt], "pca_feat": Xfeat_tgt[idxt]}, verbose=0)
emb_src_after  = feat_model_after .predict({"signal": Xs_te[idxs], "pca_feat": Xf_te[idxs]}, verbose=0)
emb_tgt_after  = feat_model_after .predict({"signal": Xsig_tgt[idxt], "pca_feat": Xfeat_tgt[idxt]}, verbose=0)

def plot_tsne(emb_s, emb_t, title, fname):
    X = np.vstack([emb_s, emb_t])
    y_dom = np.array([0]*len(emb_s) + [1]*len(emb_t))
    X_tsne = TSNE(n_components=2, perplexity=30, init="pca", n_iter=1000, random_state=42).fit_transform(X)
    plt.figure(figsize=(6.8,5.2))
    plt.scatter(X_tsne[y_dom==0,0], X_tsne[y_dom==0,1], s=14, alpha=0.85, label="源域", marker='o')
    plt.scatter(X_tsne[y_dom==1,0], X_tsne[y_dom==1,1], s=14, alpha=0.85, label="目标域", marker='^')
    plt.legend()
    plt.title(title); plt.xlabel("t-SNE 1"); plt.ylabel("t-SNE 2")
    plt.tight_layout(); plt.savefig(fname); plt.show()

plot_tsne(emb_src_before, emb_tgt_before, "对齐之前的嵌入分布（源 vs 目标）", "tSNE_对齐前.png")
plot_tsne(emb_src_after,  emb_tgt_after,  "对齐之后的嵌入分布（源 vs 目标）", "tSNE_对齐后.png")

def rbf_mmd2(X, Y, gamma=None):
    X = np.asarray(X); Y = np.asarray(Y)
    n, m = X.shape[0], Y.shape[0]
    if gamma is None:
        Z = np.vstack([X[np.random.choice(n, min(n,200), replace=False)],
                       Y[np.random.choice(m, min(m,200), replace=False)]])
        d = np.sum((Z[:,None,:]-Z[None,:,:])**2, axis=-1)
        med = np.median(d[d>0]); gamma = 1.0/(med+1e-9)
    Kxx = np.exp(-gamma * ((X[:,None,:]-X[None,:,:])**2).sum(-1))
    Kyy = np.exp(-gamma * ((Y[:,None,:]-Y[None,:,:])**2).sum(-1))
    Kxy = np.exp(-gamma * ((X[:,None,:]-Y[None,:,:])**2).sum(-1))
    return float(Kxx.mean() + Kyy.mean() - 2*Kxy.mean())

mmd_before = rbf_mmd2(emb_src_before, emb_tgt_before)
mmd_after  = rbf_mmd2(emb_src_after,  emb_tgt_after)

plt.figure(figsize=(5.6,3.6))
plt.bar(["对齐前","对齐后"], [mmd_before, mmd_after])
plt.ylabel("MMD^2（越小越好）"); plt.title("域差异的 MMD 量化对比")
plt.tight_layout(); plt.savefig("MMD_对比.png"); plt.show()

with open("DANN_训练与对齐_摘要.txt", "w", encoding="utf-8") as f:
    f.write("【DANN 训练摘要】\n")
    f.write(f"源域测试集：Acc={acc_src:.4f}, Macro-F1={f1_src:.4f}\n")
    f.write(f"MMD：对齐前={mmd_before:.6f}，对齐后={mmd_after:.6f}\n")
    f.write(f"域判别准确率：{np.mean(hist_dom_acc[-steps_per_epoch:]):.4f}\n")
    f.write(f"是否为代理目标域：{USED_PROXY_TARGET}\n")

dann_model.save("双流1D-CNN_DANN.h5")

# CELL 1
