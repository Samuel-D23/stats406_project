import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


# 读取CSV文件
df1 = pd.read_csv('/Users/samuelchen/Desktop/dataset/2019.csv')
df2 = pd.read_csv('/Users/samuelchen/Desktop/dataset/2020.csv')

# 合并两个数据集
df = pd.concat([df1, df2])

# 将日期从字符串转换为日期对象
df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')

# 添加一个通用年份列，以便对齐数据
df['common_date'] = df['date'].apply(lambda x: x.replace(year=2020))

# 以城市分组
cities = df.groupby('city')

# 为每个城市绘图
for city, data in cities:
    # 排序数据
    data = data.sort_values('common_date')
    
    # 筛选数据
    data_2018_2019 = data[(data['date'] >= '2018-12-01') & (data['date'] <= '2019-06-30')]
    data_2019_2020 = data[(data['date'] >= '2019-12-01') & (data['date'] <= '2020-06-30')]
    
    # 绘制图形
    plt.figure(figsize=(10,5))
    plt.plot(data_2018_2019['common_date'], data_2018_2019['AQI_avg'], linestyle='--', label='2018-12 to 2019-06')
    plt.plot(data_2019_2020['common_date'], data_2019_2020['AQI_avg'], linestyle='-', label='2019-12 to 2020-06')
    
    plt.title(f'AQI Time Series for {city}')
    plt.xlabel('Date')
    plt.ylabel('AQI Value')
    
    # 设置横轴格式，仅显示月和日
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    
    # 设置图例
    plt.legend()
    
    # 旋转日期标签以避免重叠
    plt.gcf().autofmt_xdate()
    
    plt.tight_layout()
    
    # 保存图形
    plt.savefig(f'AQI_{city}.png')
    plt.close()  # 关闭图形