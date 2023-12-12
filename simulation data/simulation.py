import os
import pandas as pd
import numpy as np

# 定义计算AQI的函数
def calculate_aqi_from_pm2_5(pm2_5):
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
    else:
        return 300 + (pm2_5 - 250) * (100 / 150)

# 设置文件夹路径
folder_path = '/Users/samuelchen/Desktop/UMICH/STATS 406/stats406_project/cleaned data'

# 获取文件夹中的所有文件名
file_names = os.listdir(folder_path)

# 初始化一个空列表来存储每个城市的模拟结果
all_cities_simulation_results = []

# 循环处理每个文件
for file_name in file_names:
    # 读取数据
    file_path = os.path.join(folder_path, file_name)
    city_data = pd.read_excel(file_path, sheet_name='2019_B')
    city_data['date'] = pd.to_datetime(city_data['date'])

    # 模拟测试
    simulation_results = []
    for _ in range(1000):
        reduction_percentage = np.random.uniform(0.1, 0.2)
        reduced_pm2_5 = city_data['PM_2_5'] * (1 - reduction_percentage)
        recalculated_aqi = reduced_pm2_5.apply(calculate_aqi_from_pm2_5)
        simulation_results.append(recalculated_aqi.mean())

    # 获取城市名称（从文件名"CityName_data_2019.xlsx"中提取）
    city_name = file_name.split('_data_')[0]

    # 添加结果到列表
    all_cities_simulation_results.append({
        'City': city_name,
        'Mean AQI': np.mean(simulation_results),
        'Std AQI': np.std(simulation_results),
        'Min AQI': np.min(simulation_results),
        'Max AQI': np.max(simulation_results)
    })

# 创建DataFrame并保存到Excel文件
results_df = pd.DataFrame(all_cities_simulation_results)
results_df.to_excel('/Users/samuelchen/Desktop/UMICH/STATS 406/stats406_project/simulation data/simulation_results.xlsx', index=False)

print("Simulation results saved to Excel.")
