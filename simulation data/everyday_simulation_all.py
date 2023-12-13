import pandas as pd
import numpy as np
import os

# 读取上传的数据文件
file_path = '/Users/samuelchen/Desktop/UMICH/STATS 406/stats406_project/cleaned data/Zhengzhou_data_2019.xlsx'
wuhan_data = pd.read_excel(file_path)

# 您提供的AQI子指数计算函数
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

# 确保日期格式正确
wuhan_data['date'] = pd.to_datetime(wuhan_data['date'])

# 初始化存储模拟AQI结果的列
wuhan_data['Simulated_AQI'] = 0

# 对每一行数据进行模拟测试
for index, row in wuhan_data.iterrows():
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
    wuhan_data.at[index, 'Simulated_AQI'] = np.mean(simulation_results)

# 保存到新的Excel文件
output_file_path_sheet_b = '/Users/samuelchen/Desktop/UMICH/STATS 406/stats406_project/simulation data/simulation_everyday_all/Zhengzhou_data_2019_B_with_Simulated_AQI.xlsx'
wuhan_data.to_excel(output_file_path_sheet_b, index=False)