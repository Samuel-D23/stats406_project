import pandas as pd
import os

directory_path = '/Users/samuelchen/Desktop/city daily/2020'

# List all files in the directory and sort them
# This assumes that the file naming convention is consistent and all files are CSVs
all_csv_files = sorted([
    os.path.join(directory_path, file)
    for file in os.listdir(directory_path)
    if file.endswith('.csv')
])

# Filter out the previously combined file from the list
csv_files_to_combine = [
    file for file in all_csv_files if "combined_china_cities" not in file
]

# Concatenate the CSV files into one DataFrame
# Since there can be many files and to be memory efficient, we'll use a generator expression
combined_df_large = pd.concat((pd.read_csv(file) for file in csv_files_to_combine), ignore_index=True)

# Save the combined DataFrame to a new CSV file
combined_csv_path_large = "/Users/samuelchen/Desktop/combined_china_cities_2020.csv"
combined_df_large.to_csv(combined_csv_path_large, index=False)


