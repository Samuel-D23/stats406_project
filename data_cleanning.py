
import pandas as pd
import os

# 你存放原始CSV文件的文件夹路径
input_folder_path = '/Users/samuelchen/Desktop/city'

# 你想要保存新CSV文件的文件夹路径
output_folder_path = '/Users/samuelchen/Desktop/cityed'

# 创建输出文件夹（如果它不存在的话）
if not os.path.exists(output_folder_path):
    os.makedirs(output_folder_path)
    
city_name_mapping = {
    '北京': 'Beijing', '天津': 'Tianjin', '上海': 'Shanghai', '重庆': 'Chongqing',
    '石家庄': 'Shijiazhuang', '太原': 'Taiyuan', '呼和浩特': 'Hohhot',
    '沈阳': 'Shenyang', '长春': 'Changchun', '哈尔滨': 'Harbin',
    '南京': 'Nanjing', '杭州': 'Hangzhou', '合肥': 'Hefei',
    '福州': 'Fuzhou', '济南': 'Jinan', '南昌': 'Nanchang',
    '郑州': 'Zhengzhou', '乌鲁木齐': 'Urumqi', '武汉': 'Wuhan',
    '长沙': 'Changsha', '广州': 'Guangzhou', '南宁': 'Nanning',
    '海口': 'Haikou', '成都': 'Chengdu', '贵阳': 'Guiyang',
    '昆明': 'Kunming', '拉萨': 'Lhasa', '西安': 'Xi\'an',
    '西宁': 'Xining', '兰州': 'Lanzhou', '银川': 'Yinchuan'
}

# 需要保留的城市拼音列表
pinyin_city_names = list(city_name_mapping.values())

# 遍历文件夹中的每个CSV文件
for filename in os.listdir(input_folder_path):
    if filename.endswith('.csv'):  # 确保只处理CSV文件
        input_file_path = os.path.join(input_folder_path, filename)
        data = pd.read_csv(input_file_path)

        # 将城市名称转换为拼音
        data['城市'] = data['城市'].map(city_name_mapping.get)

        # 重命名列名称从'城市'到'city'
        data.rename(columns={'城市': 'city'}, inplace=True)

        # 筛选出指定城市的数据
        filtered_data = data[data['city'].isin(pinyin_city_names)]

        # 保存清洗后的数据到新文件夹
        output_file_path = os.path.join(output_folder_path, f'filtered_{filename}')
        filtered_data.to_csv(output_file_path, index=False)

# 打印完成信息
print("All files have been processed and saved to the new folder.")

