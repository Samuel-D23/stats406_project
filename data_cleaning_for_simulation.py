import pandas as pd
import os

# Load the Excel file
file_path = '/Users/samuelchen/Desktop/UMICH/STATS 406/stats406_project/city daily/combined_china_cities_2019.csv'
data = pd.read_csv(file_path)

# Get a list of unique cities
cities = data['city'].unique()

# Define date ranges for each sheet
date_ranges = {
    '2019_A': (20181201, 20190131),
    '2019_B': (20190201, 20190430),
    '2019_C': (20190501, 20190630)
}

# Function to filter data based on date range
def filter_data_by_date_range(df, start_date, end_date):
    return df[(df['date'] >= start_date) & (df['date'] <= end_date)]

# Output folder for the Excel files
output_folder = '/Users/samuelchen/Desktop/UMICH/STATS 406/stats406_project/simulation test'
os.makedirs(output_folder, exist_ok=True)

# Process data for each city and save to separate Excel files
for city in cities:
    city_data = data[data['city'] == city]
    output_file_path = os.path.join(output_folder, f'{city}_data_2019.xlsx')
    
    with pd.ExcelWriter(output_file_path, engine='xlsxwriter') as writer:
        for sheet, date_range in date_ranges.items():
            sheet_data = filter_data_by_date_range(city_data, *date_range)
            sheet_data.to_excel(writer, sheet_name=sheet, index=False)
