import pandas as pd

# Read data from the input CSV
input_file = 'data/cleaned/200-response_time_clean.csv'
output_file = 'data/average/response_time/response_time_average.csv'

# Load the CSV into a DataFrame
df = pd.read_csv(input_file)

# Define the columns for calculation
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

# Initialize a dictionary to store weighted averages
weighted_averages = {}

# Calculate weighted averages
for response_time_col, vus_col in zip(response_time_columns, vus_columns):
    total_weighted_time = (df[response_time_col] * df[vus_col]).sum()
    total_users = df[vus_col].sum()
    weighted_averages[response_time_col] = (
        total_weighted_time / total_users if total_users > 0 else 0
    )

# Save the result to a new CSV
result_df = pd.DataFrame([weighted_averages])
result_df.to_csv(output_file, index=False)

print(f"Weighted averages written to {output_file}")