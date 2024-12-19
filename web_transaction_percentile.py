import pandas as pd

# Input and output file names
input_file = 'data/cleaned/200-web_transaction_time_clean.csv'
output_high_file = 'data/percentiles/web_transaction_time/web_transaction_time_highs.csv'
output_low_file = 'data/percentiles/web_transaction_time/web_transaction_time_lows.csv'

# Load the CSV into a DataFrame
df = pd.read_csv(input_file)

# Define the columns for transaction times and user counts
transaction_time_columns = [
    "micro_web_transaction_time",
    "mono_web_transaction_time",
    "hybrid_web_transaction_time",
    "dist_micro_web_transaction_time",
    "dist_mono_web_transaction_time",
    "dist_hybrid_web_transaction_time",
]

vus_columns = [
    "micro_vus",
    "mono_vus",
    "hybrid_vus",
    "dist_micro_vus",
    "dist_mono_vus",
    "dist_hybrid_vus",
]

# Function to calculate weighted percentiles
def weighted_percentile(data, weights, percent):
    sorted_indices = data.argsort()
    sorted_data = data[sorted_indices]
    sorted_weights = weights[sorted_indices]
    cumulative_weights = sorted_weights.cumsum()
    total_weight = sorted_weights.sum()
    percentile_idx = (cumulative_weights >= percent * total_weight).argmax()
    return sorted_data[percentile_idx]

# Function to calculate percentiles for all columns
def calculate_percentiles(df):
    results = []
    for transaction_time_col, vus_col in zip(transaction_time_columns, vus_columns):
        data = df[transaction_time_col].values
        weights = df[vus_col].values
        results.append([transaction_time_col, "1% Low", weighted_percentile(data, weights, 0.01)])
        results.append([transaction_time_col, "0.1% Low", weighted_percentile(data, weights, 0.001)])
        results.append([transaction_time_col, "1% High", weighted_percentile(data, weights, 0.99)])
        results.append([transaction_time_col, "0.1% High", weighted_percentile(data, weights, 0.999)])
    return results

# Calculate percentiles
percentile_results = calculate_percentiles(df)

# Convert the results to DataFrames
percentile_df = pd.DataFrame(percentile_results, columns=["Metric", "Percentile", "Value"])

# Split into high and low percentiles
low_percentiles = percentile_df[percentile_df["Percentile"].str.contains("Low")]
high_percentiles = percentile_df[percentile_df["Percentile"].str.contains("High")]

# Save to CSV files with headers
low_percentiles.to_csv(output_low_file, index=False)
high_percentiles.to_csv(output_high_file, index=False)

print(f"High percentiles written to {output_high_file}")
print(f"Low percentiles written to {output_low_file}")
