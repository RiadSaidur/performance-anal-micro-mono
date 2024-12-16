import csv

# Read the CSV file
with open("data/cleaned/200-web_transaction_time_clean.csv", "r") as file:
    reader = csv.reader(file)
    header = next(reader)  # Read the header row

    # Initialize variables to calculate sums and counts for each column
    sums = [0] * (len(header) - 1)
    counts = [0] * (len(header) - 1)

    for row in reader:
        for i in range(1, len(row)):  # Skip the timestamp column
            sums[i - 1] += float(row[i])
            counts[i - 1] += 1

# Calculate averages
averages = [s / c for s, c in zip(sums, counts)]

# Write the averages to a new CSV file
with open("data/average/web_transaction_time_total_average.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Column", "Average"])
    for col, avg in zip(header[1:], averages):
        writer.writerow([col, avg])

print("Averages calculated and saved to 'averages.csv'.")
