import pandas as pd

# Input and output file names
input_file = 'data/cleaned/200-web_transaction_time_clean.csv'
output_file = 'data/average/web_transaction_time/web_transaction_time_average.csv'

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

# Initialize a dictionary to store weighted averages
weighted_averages = {}

# Calculate weighted averages
for transaction_time_col, vus_col in zip(transaction_time_columns, vus_columns):
    total_weighted_time = (df[transaction_time_col] * df[vus_col]).sum()
    total_users = df[vus_col].sum()
    weighted_averages[transaction_time_col.replace("web_transaction_time", "avg_transaction_time")] = (
        total_weighted_time / total_users if total_users > 0 else 0
    )

# Save the result to a new CSV
result_df = pd.DataFrame([weighted_averages])
result_df.to_csv(output_file, index=False)

print(f"Weighted averages written to {output_file}")
