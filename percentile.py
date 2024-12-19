import pandas as pd
import numpy as np

# Load data from CSV
data = pd.read_csv('source/200-response_time_clean.csv')

# Define percentiles
percentiles = {
    '1% High': 0.99,
    '0.1% High': 0.999,
    '1% Low': 0.01,
    '0.1% Low': 0.001
}

# List of columns to calculate percentiles for
columns = [
    'micro_response_time', 'mono_response_time', 'hybrid_response_time',
    'dist_micro_response_time', 'dist_mono_response_time', 'dist_hybrid_response_time'
]

# Create dictionaries to store results for highs and lows
highs = {'Metric': [], 'Percentile': [], 'Value': []}
lows = {'Metric': [], 'Percentile': [], 'Value': []}

# Calculate weighted percentiles for each column
for column in columns:
    # Determine the corresponding _vus column
    vus_column = column.replace('response_time', 'vus')

    if vus_column not in data.columns:
        raise ValueError(f"The dataset must include a '{vus_column}' column for accurate weighting.")

    for percentile_name, percentile_value in percentiles.items():
        # Sort by column values and calculate cumulative weights
        sorted_data = data[[column, vus_column]].sort_values(by=column)
        sorted_data['weight'] = sorted_data[vus_column] / sorted_data[vus_column].sum()
        sorted_data['cum_weight'] = sorted_data['weight'].cumsum()

        # Find the weighted percentile value
        if 'High' in percentile_name:
            value = sorted_data[sorted_data['cum_weight'] >= percentile_value][column].iloc[0]
            highs['Metric'].append(column)
            highs['Percentile'].append(percentile_name)
            highs['Value'].append(value)
        elif 'Low' in percentile_name:
            value = sorted_data[sorted_data['cum_weight'] <= percentile_value][column].iloc[-1]
            lows['Metric'].append(column)
            lows['Percentile'].append(percentile_name)
            lows['Value'].append(value)

# Convert results to DataFrames
highs_df = pd.DataFrame(highs)
lows_df = pd.DataFrame(lows)

# Save results to separate CSVs
highs_df.to_csv('percentiles/response_time_highs.csv', index=False)
lows_df.to_csv('percentiles/response_time_lows.csv', index=False)
