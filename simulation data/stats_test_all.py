# 导入必要的库
import pandas as pd
import numpy as np
from scipy.stats import shapiro, mannwhitneyu

# 定义计算AQI子指数的函数
def calculate_subindex_pm2_5(pm2_5):
    if pm2_5 <= 35:
        return pm2_5 * (50 / 35)
    elif pm2_5 <= 75:
        return 50 + (pm2_5 - 35) * (50 / 40)
    elif pm2_5 <= 115:
        return 100 + (pm2_5 - 75) * (50 / 40)
    elif pm2_5 <= 150:
        return 150 + (pm2_5 - 115) * (100 / 35)
    elif pm2_5 <= 250:
        return 200 + (pm2_5 - 150) * (100 / 100)
    elif pm2_5 <= 350:
        return 300 + (pm2_5 - 250) * (100 / 100)
    elif pm2_5 <= 500:
        return 400 + (pm2_5 - 350) * (100 / 150)
    else:
        return 500

def calculate_subindex_pm10(pm10):
    if pm10 <= 50:
        return pm10 * (50 / 50)
    elif pm10 <= 150:
        return 50 + (pm10 - 50) * (50 / 100)
    elif pm10 <= 250:
        return 100 + (pm10 - 150) * (50 / 100)
    elif pm10 <= 350:
        return 150 + (pm10 - 250) * (100 / 100)
    elif pm10 <= 420:
        return 200 + (pm10 - 350) * (100 / 70)
    elif pm10 <= 500:
        return 300 + (pm10 - 420) * (100 / 80)
    elif pm10 <= 600:
        return 400 + (pm10 - 500) * (100 / 100)
    else:
        return 500

def calculate_subindex_so2(so2):
    if so2 <= 50:
        return so2 * (50 / 50)
    elif so2 <= 150:
        return 50 + (so2 - 50) * (50 / 100)
    elif so2 <= 475:
        return 100 + (so2 - 150) * (50 / 325)
    elif so2 <= 800:
        return 150 + (so2 - 475) * (100 / 325)
    elif so2 <= 1600:
        return 200 + (so2 - 800) * (100 / 800)
    elif so2 <= 2100:
        return 300 + (so2 - 1600) * (100 / 500)
    elif so2 <= 2620:
        return 400 + (so2 - 2100) * (100 / 520)
    else:
        return 500

def calculate_subindex_no2(no2):
    if no2 <= 40:
        return no2 * (50 / 40)
    elif no2 <= 80:
        return 50 + (no2 - 40) * (50 / 40)
    elif no2 <= 180:
        return 100 + (no2 - 80) * (50 / 100)
    elif no2 <= 280:
        return 150 + (no2 - 180) * (100 / 100)
    elif no2 <= 565:
        return 200 + (no2 - 280) * (100 / 285)
    elif no2 <= 750:
        return 300 + (no2 - 565) * (100 / 185)
    elif no2 <= 940:
        return 400 + (no2 - 750) * (100 / 190)
    else:
        return 500


# 继续定义剩余的计算AQI子指数的函数
def calculate_subindex_co(co):
    if co <= 2:
        return co * (50 / 2)
    elif co <= 4:
        return 50 + (co - 2) * (50 / 2)
    elif co <= 14:
        return 100 + (co - 4) * (50 / 10)
    elif co <= 24:
        return 150 + (co - 14) * (100 / 10)
    elif co <= 36:
        return 200 + (co - 24) * (100 / 12)
    elif co <= 48:
        return 300 + (co - 36) * (100 / 12)
    elif co <= 60:
        return 400 + (co - 48) * (100 / 12)
    else:
        return 500

def calculate_subindex_o3(o3):
    if o3 <= 100:
        return o3 * (50 / 100)
    elif o3 <= 160:
        return 50 + (o3 - 100) * (50 / 60)
    elif o3 <= 215:
        return 100 + (o3 - 160) * (50 / 55)
    elif o3 <= 265:
        return 150 + (o3 - 215) * (100 / 50)
    elif o3 <= 800:
        return 200 + (o3 - 265) * (100 / 535)
    elif o3 <= 1000:
        return 300 + (o3 - 800) * (100 / 200)
    elif o3 <= 1200:
        return 400 + (o3 - 1000) * (100 / 200)
    else:
        return 500

# 读取2019年的数据
file_path_2019 = '/Users/samuelchen/Desktop/UMICH/STATS 406/stats406_project/cleaned data/Jinan_data_2019.xlsx'
wuhan_data_2019 = pd.read_excel(file_path_2019)

# 确保日期格式正确
wuhan_data_2019['date'] = pd.to_datetime(wuhan_data_2019['date'])

# 初始化存储模拟AQI结果的列
wuhan_data_2019['Simulated_AQI'] = 0

# 对每一行数据进行模拟测试
for index, row in wuhan_data_2019.iterrows():
    simulation_results = []
    for _ in range(1000):
        # 模拟减少污染物的浓度
        reduced_pm2_5 = row['PM_2_5'] * (1 - np.random.uniform(0.1, 0.2))
        reduced_pm10 = row['PM_10'] * (1 - np.random.uniform(0.1, 0.2))
        reduced_so2 = row['SO_2'] * (1 - np.random.uniform(0.1, 0.2))
        reduced_no2 = row['NO_2'] * (1 - np.random.uniform(0.1, 0.2))
        reduced_co = row['CO'] * (1 - np.random.uniform(0.1, 0.2))
        reduced_o3 = row['O3_8h_max'] * (1 - np.random.uniform(0.1, 0.2))

        # 计算模拟AQI
        simulated_aqi = max(
            calculate_subindex_pm2_5(reduced_pm2_5),
            calculate_subindex_pm10(reduced_pm10),
            calculate_subindex_so2(reduced_so2),
            calculate_subindex_no2(reduced_no2),
            calculate_subindex_co(reduced_co),
            calculate_subindex_o3(reduced_o3)
        )
        simulation_results.append(simulated_aqi)
    
    # 将1000次模拟的平均值作为该行的模拟AQI
    wuhan_data_2019.at[index, 'Simulated_AQI'] = np.mean(simulation_results)

# 保存到新的Excel文件
output_file_2019 = '/Users/samuelchen/Desktop/UMICH/STATS 406/stats406_project/simulation data/simulation_everyday_all/Jinan_data_2019_B_with_Simulated_AQI.xlsx'
wuhan_data_2019.to_excel(output_file_2019, index=False)

# 读取2020年的数据，第二个sheet
file_path_2020 = '/Users/samuelchen/Desktop/UMICH/STATS 406/stats406_project/cleaned data 2020/Jinan_data_2020.xlsx'
wuhan_data_2020 = pd.read_excel(file_path_2020, sheet_name=1)

# 继续进行正态性检验和非参数检验的代码
simulated_aqi_2019 = wuhan_data_2019['Simulated_AQI']
actual_aqi_2020 = wuhan_data_2020['AQI_avg']

# Shapiro-Wilk test for normality
shapiro_test_2019 = shapiro(simulated_aqi_2019)
shapiro_test_2020 = shapiro(actual_aqi_2020)

# Mann-Whitney U test
min_length = min(len(simulated_aqi_2019), len(actual_aqi_2020))
simulated_aqi_2019_aligned = simulated_aqi_2019[:min_length]
actual_aqi_2020_aligned = actual_aqi_2020[:min_length]
mannwhitneyu_result = mannwhitneyu(simulated_aqi_2019_aligned, actual_aqi_2020_aligned)

# Print the results
print("Shapiro Test 2019:", shapiro_test_2019)
print("Shapiro Test 2020:", shapiro_test_2020)
print("Mann-Whitney U Test Result:", mannwhitneyu_result)

