import pandas as pd
import matplotlib.pyplot as plt
import pywt
import numpy as np

# 读取上传的CSV文件
file_path = 'IR014_1data.csv'
data = pd.read_csv(file_path)

# 显示数据的前几行以确认内容
data.head()

import pandas as pd


# 定义小波变换函数
def wavelet_denoise(data, wavelet='db1', level=1):
    # Decompose to get the wavelet coefficients
    coeffs = pywt.wavedec(data, wavelet, level=level)

    # Threshold the coefficients to remove noise
    threshold = np.std(coeffs[-1]) * np.sqrt(2 * np.log(len(data)))
    coeffs_thresholded = [pywt.threshold(c, threshold, mode='soft') for c in coeffs]

    # Reconstruct the signal from the thresholded coefficients
    data_denoised = pywt.waverec(coeffs_thresholded, wavelet)
    return data_denoised

import pandas as pd
import numpy as np

np.random.seed(0)
time = np.linspace(0, 1, 192000)
X175DEtime =data['X175_DE_time']
X175FEtime =data['X175_FE_time']


# 储存去噪数据
data = pd.DataFrame({'X175DEtime': X175DEtime, 'X175FEtime': X175FEtime})

X175DEtime_denoised = wavelet_denoise(data['X175DEtime'].values)
X175FEtime_denoised = wavelet_denoise(data['X175FEtime'].values)

denoised_data = pd.DataFrame({'X175DEtime_denoised': X175DEtime_denoised, 'X175FEtime_denoised': X175FEtime_denoised})
denoised_data.to_csv("IR014_1小波.csv")
# 小波变换后数据展示
denoised_data.head()
import matplotlib.pyplot as plt

# 去噪前后对比图
plt.figure(figsize=(12, 8))
# X175DEtime
plt.subplot(2, 1, 1)
plt.plot(time,data['X175DEtime'], label='Original X175DEtime')
plt.plot(time,denoised_data['X175DEtime_denoised'], label='Denoised X175DEtime', linewidth=2)
plt.legend()
plt.title('X175DEtime - Original vs Denoised')

# X175FEtime
plt.subplot(2, 1, 2)
plt.plot(time, data['X175FEtime'], label='Original X175FEtime')
plt.plot(time, denoised_data['X175FEtime_denoised'], label='Denoised X175FEtime', linewidth=2)
plt.legend()
plt.title('X175FEtime - Original vs Denoised')

plt.tight_layout()
plt.show()


