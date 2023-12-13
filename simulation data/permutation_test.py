import pandas as pd
import numpy as np


# 定义计算PM2.5子指数的函数
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

# 加载数据
file_path = '/Users/samuelchen/Desktop/UMICH/STATS 406/stats406_project/cleaned data/Wuhan_data_2019.xlsx'
wuhan_data = pd.read_excel(file_path, sheet_name='2019_B')

# 确保日期格式正确
wuhan_data['date'] = pd.to_datetime(wuhan_data['date'])

# 蒙特卡洛模拟
num_simulations = 1000
daily_aqi_means = []

for _, row in wuhan_data.iterrows():
    simulation_aqis = []
    for _ in range(num_simulations):
        reduction_percentage = np.random.uniform(0.1, 0.2)
        reduced_pm2_5 = row['PM_2_5'] * (1 - reduction_percentage)
        aqi = calculate_subindex_pm2_5(reduced_pm2_5)
        simulation_aqis.append(aqi)
    daily_aqi_means.append(np.mean(simulation_aqis))

# 添加模拟AQI平均值到数据中
wuhan_data['AQI_reduced'] = daily_aqi_means

# 排列检验
num_permutations = 1000
permutation_stats = []

original_stat = np.abs(wuhan_data['AQI_avg'].mean() - wuhan_data['AQI_reduced'].mean())

for _ in range(num_permutations):
    shuffled_aqi = np.random.permutation(np.concatenate([wuhan_data['AQI_avg'], wuhan_data['AQI_reduced']]))
    group_a = shuffled_aqi[:len(shuffled_aqi) // 2]
    group_b = shuffled_aqi[len(shuffled_aqi) // 2:]
    new_stat = np.abs(np.mean(group_a) - np.mean(group_b))
    permutation_stats.append(new_stat)

# 计算P值
p_value = np.mean(np.array(permutation_stats) >= original_stat)

print(f"Original Statistic: {original_stat}")
print(f"P-value: {p_value}")

