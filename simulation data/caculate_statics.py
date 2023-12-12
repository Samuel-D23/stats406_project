import pandas as pd
import statsmodels.api as sm
from statsmodels.stats.power import TTestIndPower

# Load and consolidate the datasets
file_paths = [
    '/path/to/Fuzhou_data_2019.xlsx',
    '/path/to/Guiyang_data_2019.xlsx',
    '/path/to/Hangzhou_data_2019.xlsx',
    '/path/to/Harbin_data_2019.xlsx',
    '/path/to/Jinan_data_2019.xlsx',
    '/path/to/Kunming_data_2019.xlsx',
    '/path/to/Shanghai_data_2019.xlsx',
    '/path/to/Shijiazhuang_data_2019.xlsx',
    '/path/to/Wuhan_data_2019.xlsx',
    '/path/to/Zhengzhou_data_2019.xlsx'
]

consolidated_data = pd.DataFrame()
for file_path in file_paths:
    city_name = file_path.split('/')[-1].split('_')[0]  # Extract city name from file path
    city_data = pd.read_excel(file_path)
    city_data_subset = city_data[['city', 'date', 'PM_2_5', 'AQI_avg']].copy()
    city_data_subset['city'] = city_name  # Ensure city name is correctly set
    consolidated_data = pd.concat([consolidated_data, city_data_subset])

# Reset index after concatenation
consolidated_data.reset_index(drop=True, inplace=True)

# Prepare the data for regression analysis
X = consolidated_data['PM_2_5']  # Predictor variable: PM2.5
y = consolidated_data['AQI_avg']  # Response variable: AQI
X = sm.add_constant(X)  # Adding a constant for the intercept

# Perform the regression analysis
model = sm.OLS(y, X).fit()

# Power of the test
effect_size = (model.params['PM_2_5'] / model.bse['PM_2_5'])
power_analysis = TTestIndPower()
power = power_analysis.solve_power(effect_size=effect_size, nobs1=len(X), alpha=0.05, ratio=1, alternative='larger')

# Bias (Mean of residuals)
bias = model.resid.mean()

# Mean Squared Error (MSE)
mse = (model.resid ** 2).mean()

# Output the results
print(f"Power of the Test: {power}")
print(f"Bias: {bias}")
print(f"Mean Squared Error (MSE): {mse}")
