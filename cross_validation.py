from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import KFold
import numpy as np
import pandas as pd

# Load the uploaded CSV file
file_path = '/Users/samuelchen/Desktop/UMICH/STATS 406/stats406_project/city daily/combined_china_cities_2019.csv'
data = pd.read_csv(file_path)

# Dropping rows with missing values
data_cleaned = data.dropna()

# Selecting predictor variables and target variable
X = data_cleaned[['SO_2', 'NO_2', 'CO', 'PM_10', 'PM_2_5', 'O3_8h_max']]
y = data_cleaned['AQI_avg']

# Initialize linear regression model
model = LinearRegression()

# Setting up K-Fold cross-validation
kf = KFold(n_splits=5, shuffle=True, random_state=42)

# Apply K-Fold cross-validation
cv_scores = cross_val_score(model, X, y, cv=kf, scoring='neg_mean_squared_error')

# Calculate average RMSE across all folds
rmse_scores = np.sqrt(-cv_scores)
average_rmse = np.mean(rmse_scores)

print(average_rmse)

