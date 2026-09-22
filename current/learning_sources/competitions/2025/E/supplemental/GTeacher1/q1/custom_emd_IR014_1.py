import numpy as np
import pandas as pd
from scipy.interpolate import CubicSpline
import matplotlib.pyplot as plt
def find_extrema(x, y):
    dy = np.diff(y)
    ddy = np.diff(dy)
    extrema = []
    for i in range(1, len(dy) - 1):
        if dy[i] * dy[i - 1] < 0:
            extrema.append((x[i], y[i]))
    return extrema

def interpolate_extrema(extrema, x):
    if len(extrema) < 2:
        return np.zeros_like(x)
    x_ext, y_ext = zip(*extrema)
    cs = CubicSpline(x_ext, y_ext, bc_type='natural')
    return cs(x)

def emd(signal, max_imf=8, tol=0.1):
    imfs = []
    residue = signal
    while len(imfs) < max_imf:
        h = residue
        sd = np.inf
        while sd > tol:
            extrema = find_extrema(np.arange(len(h)), h)
            max_env = interpolate_extrema(extrema, np.arange(len(h)))
            min_env = -interpolate_extrema([ext for ext in extrema if ext[1] < 0], np.arange(len(h)))
            mean_env = (max_env + min_env) / 2
            h_new = h - mean_env
            sd = np.sum((h - h_new) ** 2) / np.sum(h ** 2)
            h = h_new
        imfs.append(h)
        residue -= h
        if np.all(residue < tol):
            break
    return imfs, residue


df = pd.read_csv('IR014_1小波.csv')

# Assume the signal is in the second column (index 1)
signal = df.iloc[:, 1].values

#计算EMD
imfs, residue = emd(signal)


for i, imf in enumerate(imfs):
    print(f"IMF {i+1}:")
    print(imf)
print("Residue:")
print(residue)

# 加载CSV文件
df = pd.read_csv('IR014_1小波.csv')

# 假设我们要分析的信号在第二列（索引为1）
signal = df.iloc[:, 1].values

# Perform EMD
imfs, residue = emd(signal)

# 绘制原始信号
plt.figure(figsize=(12, 9))
plt.subplot(len(imfs) + 2, 1, 1)
plt.plot(signal, 'r')
plt.title("Original Signal")

# 绘制每个IMF
for i, imf in enumerate(imfs):
    plt.subplot(len(imfs) + 2, 1, i + 2)
    plt.plot(imf, 'g')
    plt.title(f"IMF {i + 1}")

# 绘制残余项
plt.subplot(len(imfs) + 2, 1, len(imfs) + 2)
plt.plot(residue, 'b')
plt.title("Residue")

# 显示图形
plt.tight_layout()
plt.show()

# 加载数据
df = pd.read_csv('IR014_1小波.csv')
signal = df.iloc[:, 2].values

# EMD分解（假设已有emd函数）
imfs, residue = emd(signal)

# 去除基频（这里以去除残余项为例）
denoised_signal = np.sum(imfs, axis=0)

# 绘图对比
plt.figure(figsize=(12, 6))
plt.plot(signal, label='原始信号')
plt.plot(denoised_signal, label='去除基频后信号')
plt.legend()
plt.title("去除基频效果对比")
plt.show()
