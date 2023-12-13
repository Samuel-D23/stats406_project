import pandas as pd
import numpy as np

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
file_path = '/Users/samuelchen/Desktop/UMICH/STATS 406/stats406_project/cleaned data/Zhengzhou_data_2019.xlsx'
wuhan_data_sheet_b = pd.read_excel(file_path, sheet_name='2019_B')

# Apply the simulation to each day in the DataFrame from the '2019_B' sheet
wuhan_data_sheet_b['Simulated_AQI'] = wuhan_data_sheet_b['PM_2_5'].apply(simulate_daily_aqi)

# Save the modified DataFrame from the '2019_B' sheet to a new Excel file
output_file_path_sheet_b = '/Users/samuelchen/Desktop/UMICH/STATS 406/stats406_project/simulation data/simulation_everyday/Zhengzhou_data_2019_B_with_Simulated_AQI.xlsx'
wuhan_data_sheet_b.to_excel(output_file_path_sheet_b, index=False)