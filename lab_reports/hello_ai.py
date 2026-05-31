import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Step 1: Create a sample CSV file with rainfall data
# Columns: date (YYYY-MM-DD), rainfall_mm (daily precipitation), location (station name)
np.random.seed(42)
start_date = datetime(2024, 1, 1)
locations = ["Station_A", "Station_B", "Station_C"]
records = []

for i in range(30):
    date = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
    for loc in locations:
        rainfall = round(np.random.exponential(scale=5.0), 1)
        records.append([date, rainfall, loc])

df_sample = pd.DataFrame(records, columns=["date", "rainfall_mm", "location"])
csv_path = "rainfall_data.csv"
df_sample.to_csv(csv_path, index=False)
print(f"Created {csv_path} with {len(df_sample)} records\n")

# Step 2: Read the CSV file into a pandas DataFrame
df = pd.read_csv(csv_path)
print("First 5 rows of the dataset:")
print(df.head(), "\n")

# Step 3: Calculate total and average rainfall per location
summary = df.groupby("location")["rainfall_mm"].agg(["sum", "mean"]).round(2)
summary.columns = ["total_rainfall_mm", "avg_daily_rainfall_mm"]

# Step 4: Print a formatted summary report
print("=" * 50)
print("RAINFALL SUMMARY REPORT")
print("=" * 50)
print(f"Date range: {df['date'].min()} to {df['date'].max()}")
print(f"Total records: {len(df)}\n")

for loc in summary.index:
    print(f"Location: {loc}")
    print(f"  Total rainfall:     {summary.loc[loc, 'total_rainfall_mm']} mm")
    print(f"  Average daily:      {summary.loc[loc, 'avg_daily_rainfall_mm']} mm/day\n")

print(f"Overall average rainfall: {df['rainfall_mm'].mean():.2f} mm/day")
print(f"Maximum daily rainfall:   {df['rainfall_mm'].max():.1f} mm")
