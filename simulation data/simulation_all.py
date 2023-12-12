import os
import pandas as pd
import numpy as np

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
# 设置文件夹路径（替换成您文件夹的实际路径）
folder_path = '/Users/samuelchen/Desktop/UMICH/STATS 406/stats406_project/cleaned data'

# 获取文件夹中的所有文件名
file_names = os.listdir(folder_path)

# 初始化一个DataFrame来存储所有城市的模拟结果
all_cities_results = pd.DataFrame()

# 循环处理每个文件
for file_name in file_names:
    # 跳过非Excel文件
    if not file_name.endswith('.xlsx'):
        continue

    # 读取数据
    file_path = os.path.join(folder_path, file_name)
    city_data = pd.read_excel(file_path)

    # 确保日期格式正确
    city_data['date'] = pd.to_datetime(city_data['date'])

    # 模拟测试
    simulation_results = []
    for _ in range(1000):
        temp_data = city_data.copy()
        for pollutant in ['PM_2_5', 'PM_10', 'SO_2', 'NO_2', 'CO', 'O3_8h_max']:
            reduction_percentage = np.random.uniform(0.1, 0.2)
            temp_data[pollutant] *= (1 - reduction_percentage)
        temp_data['AQI'] = temp_data.apply(lambda row: max(
            calculate_subindex_pm2_5(row['PM_2_5']),
            calculate_subindex_pm10(row['PM_10']),
            calculate_subindex_so2(row['SO_2']),
            calculate_subindex_no2(row['NO_2']),
            calculate_subindex_co(row['CO']),
            calculate_subindex_o3(row['O3_8h_max'])
        ), axis=1)
        simulation_results.append(temp_data['AQI'].mean())

    # 获取城市名称
    city_name = file_name.split('_data_')[0]

    # 将结果添加到DataFrame
    city_result = pd.DataFrame({
        'City': [city_name],
        'Mean AQI': [np.mean(simulation_results)],
        'Std AQI': [np.std(simulation_results)],
        'Min AQI': [np.min(simulation_results)],
        'Max AQI': [np.max(simulation_results)]
    })
    all_cities_results = pd.concat([all_cities_results, city_result])

# 保存到Excel文件
output_file = '/Users/samuelchen/Desktop/UMICH/STATS 406/stats406_project/simulation data/simulation_results_all.xlsx'
all_cities_results.to_excel(output_file, index=False)

print("Simulation results saved to Excel.")
