import os
import pandas as pd

# 设定数据文件夹路径
data_folder_path = '/Users/samuelchen/Desktop/dataset/city 2020'  # 替换为你的数据文件夹路径

# 设定输出文件夹路径
output_folder_path = '/Users/samuelchen/Desktop/city daily/2020'  # 替换为你想保存输出文件的文件夹路径

# 创建输出文件夹（如果它不存在的话）
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)

# 遍历数据文件夹中的每个文件
for filename in os.listdir(data_folder_path):
    if filename.endswith('.csv'):
        file_path = os.path.join(data_folder_path, filename)
        
        # 读取CSV文件
        data = pd.read_csv(file_path)

        # 按城市和日期分组
        grouped_data = data.groupby(['city', 'date'])

        # 计算日平均浓度和日最大8小时平均浓度
        daily_avg_concentrations = grouped_data[['SO2', 'NO2', 'CO', 'PM10', 'PM2.5']].mean()
        daily_max_8h_o3 = grouped_data['O3_8h'].max()
        daily_avg_aqi = grouped_data['AQI'].mean()

        # 组合结果, 滑动平均值
        daily_air_quality = daily_avg_concentrations
        daily_air_quality['O3_8h_max'] = daily_max_8h_o3
        daily_air_quality['AQI_avg'] = daily_avg_aqi

        # 重置索引
        daily_air_quality.reset_index(inplace=True)

        # 更新列名
        daily_air_quality.rename(columns={
            'SO2': 'SO_2',
            'NO2': 'NO_2',
            'CO': 'CO',
            'PM10': 'PM_10',
            'PM2.5': 'PM_2_5',
            'O3_8h_max': 'O3_8h_max'
        }, inplace=True)

        # 保存处理后的数据到新的CSV文件
        output_file_path = os.path.join(output_folder_path, f'processed_{filename}')
        daily_air_quality.to_csv(output_file_path, index=False)

        print(f'Processed file saved: {output_file_path}')

print("All files have been processed.")