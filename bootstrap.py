from sklearn.utils import resample
import numpy as np
import pandas as pd

# Load the uploaded CSV file
file_path = '/Users/samuelchen/Desktop/UMICH/STATS 406/stats406_project/city daily/combined_china_cities_2019.csv'
data = pd.read_csv(file_path)

# Function to perform bootstrap resampling and calculate confidence interval
def bootstrap_confidence_interval(data, n_iterations=1000, confidence_level=0.95):
    bootstrap_means = []
    
    # Generating bootstrap samples and computing the mean of each sample
    for _ in range(n_iterations):
        sample = resample(data)
        bootstrap_means.append(sample.mean())

    # Calculating the confidence interval
    lower_percentile = ((1.0 - confidence_level) / 2.0) * 100
    upper_percentile = (confidence_level + ((1.0 - confidence_level) / 2.0)) * 100
    lower_bound = np.percentile(bootstrap_means, lower_percentile)
    upper_bound = np.percentile(bootstrap_means, upper_percentile)

    return np.mean(bootstrap_means), lower_bound, upper_bound

# Applying bootstrap to the AQI_avg column
mean_estimate, confidence_lower, confidence_upper = bootstrap_confidence_interval(data['AQI_avg'])

print(mean_estimate, confidence_lower, confidence_upper)

