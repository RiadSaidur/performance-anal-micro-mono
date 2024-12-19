import pandas as pd
from datetime import timedelta

# Input and output file names
input_file = 'data/cleaned/200-response_time_clean.csv'
output_60s_file = 'data/average/response_time/response_time_60s.csv'

# Load the CSV into a DataFrame
df = pd.read_csv(input_file)

# Convert the timestamp column to datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Define the columns for response times and user counts
response_time_columns = [
    "micro_response_time",
    "mono_response_time",
    "hybrid_response_time",
    "dist_micro_response_time",
    "dist_mono_response_time",
    "dist_hybrid_response_time",
]

vus_columns = [
    "micro_vus",
    "mono_vus",
    "hybrid_vus",
    "dist_micro_vus",
    "dist_mono_vus",
    "dist_hybrid_vus",
]

# Function to calculate weighted averages for a group
def calculate_weighted_averages(group):
    averages = {}
    for response_time_col, vus_col in zip(response_time_columns, vus_columns):
        total_weighted_time = (group[response_time_col] * group[vus_col]).sum()
        total_users = group[vus_col].sum()
        averages[response_time_col.replace("response_time", "avg_response_time")] = (
            total_weighted_time / total_users if total_users > 0 else 0
        )
    return pd.Series(averages)

# Function to group by time intervals and calculate averages
def group_and_calculate(df, interval_seconds):
    # Create a column for grouping based on time intervals
    interval_start = df['timestamp'].min()
    df['interval'] = df['timestamp'].apply(
        lambda x: interval_start + ((x - interval_start) // timedelta(seconds=interval_seconds)) * timedelta(seconds=interval_seconds)
    )
    # Group by the interval and calculate averages
    grouped = df.groupby('interval', group_keys=False).apply(calculate_weighted_averages)
    return grouped.reset_index()

# Calculate averages for 60-second intervals
result_60s = group_and_calculate(df, 60)
result_60s.to_csv(output_60s_file, index=False)
print(f"60-second interval averages written to {output_60s_file}")
