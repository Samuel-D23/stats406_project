import pandas as pd
import numpy as np
from scipy.stats import shapiro, mannwhitneyu

# Function to calculate AQI from PM2.5
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

# Function to simulate and calculate the average AQI for a day
def simulate_daily_aqi(pm2_5):
    simulation_results = []
    for _ in range(1000):
        reduction_percentage = np.random.uniform(0.1, 0.2)
        reduced_pm2_5 = pm2_5 * (1 - reduction_percentage)
        recalculated_aqi = calculate_aqi_from_pm2_5(reduced_pm2_5)
        simulation_results.append(recalculated_aqi)
    return np.mean(simulation_results)

# Load the '2019_B' sheet from the Excel file
file_path_2019 = '/Users/samuelchen/Desktop/UMICH/STATS 406/stats406_project/cleaned data/Jinan_data_2019.xlsx'
wuhan_data_sheet_b_2019 = pd.read_excel(file_path_2019, sheet_name='2019_B')

# Apply the simulation to each day in the DataFrame from the '2019_B' sheet
wuhan_data_sheet_b_2019['Simulated_AQI'] = wuhan_data_sheet_b_2019['PM_2_5'].apply(simulate_daily_aqi)

# Load the '2020_B' sheet from the Excel file for 2020 data
file_path_2020 = '/Users/samuelchen/Desktop/UMICH/STATS 406/stats406_project/cleaned data 2020/Jinan_data_2020.xlsx'
wuhan_data_2020 = pd.read_excel(file_path_2020, sheet_name='2020_B')

# Perform the Shapiro-Wilk test for normality on both datasets
simulated_aqi_2019 = wuhan_data_sheet_b_2019['Simulated_AQI']
actual_aqi_2020 = wuhan_data_2020['AQI_avg']
shapiro_test_2019 = shapiro(simulated_aqi_2019)
shapiro_test_2020 = shapiro(actual_aqi_2020)

# Prepare the data: Ensure that both datasets have the same length
min_length = min(len(simulated_aqi_2019), len(actual_aqi_2020))
simulated_aqi_2019_aligned = simulated_aqi_2019[:min_length]
actual_aqi_2020_aligned = actual_aqi_2020[:min_length]

# Perform the Mann-Whitney U test
mannwhitneyu_result = mannwhitneyu(simulated_aqi_2019_aligned, actual_aqi_2020_aligned)

# Print the results
print("Shapiro Test 2019:", shapiro_test_2019)
print("Shapiro Test 2020:", shapiro_test_2020)
print("Mann-Whitney U Test Result:", mannwhitneyu_result)
