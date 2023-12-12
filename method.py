import pandas as pd

# 载入数据
data_2019 = pd.read_csv('/Users/samuelchen/Desktop/UMICH/STATS 406/stats406_project/city daily/combined_china_cities_2019.csv')
data_2020 = pd.read_csv('/Users/samuelchen/Desktop/UMICH/STATS 406/stats406_project/city daily/combined_china_cities_2020.csv')

# 转换日期格式
data_2019['date'] = pd.to_datetime(data_2019['date'], format='%Y%m%d')
data_2020['date'] = pd.to_datetime(data_2020['date'], format='%Y%m%d')

# 定义阶段
periods = {
    '2019_A': ('2018-12-01', '2019-01-31'),
    '2019_B': ('2019-02-01', '2019-04-30'),
    '2019_C': ('2019-05-01', '2019-06-30'),
    '2020_A': ('2019-12-01', '2020-01-31'),
    '2020_B': ('2020-02-01', '2020-04-30'),
    '2020_C': ('2020-05-01', '2020-06-30')
}

# 分类每行数据到相应阶段
def categorize_period(row, year):
    for period, (start, end) in periods.items():
        if start <= row['date'].strftime('%Y-%m-%d') <= end and period.startswith(str(year)):
            return period
    return None

data_2019['period'] = data_2019.apply(lambda row: categorize_period(row, 2019), axis=1)
data_2020['period'] = data_2020.apply(lambda row: categorize_period(row, 2020), axis=1)

# 计算指标
def calculate_metrics(data):
    grouped = data.groupby(['city', 'period'])
    metrics = grouped['AQI_avg'].agg(['mean', 'max', lambda x: (x > 150).sum()])
    metrics.columns = ['AQI_mean', 'AQI_max', 'Severe_Pollution_Days']
    return metrics

metrics_2019 = calculate_metrics(data_2019)
metrics_2020 = calculate_metrics(data_2020)

# 导出到Excel
# 导出到Excel
with pd.ExcelWriter('AQI_Metrics_2019_2020.xlsx', engine='xlsxwriter') as excel_writer:
    metrics_2019.to_excel(excel_writer, sheet_name='2019 Metrics')
    metrics_2020.to_excel(excel_writer, sheet_name='2020 Metrics')

excel_writer.save()