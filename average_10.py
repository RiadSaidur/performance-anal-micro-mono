import csv
from datetime import datetime

def calculate_10sec_average(input_file, output_file):
    with open(input_file, 'r') as infile, open(output_file, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        headers = next(reader)
        writer.writerow(headers)
        
        current_start_time = None
        sums = [0.0] * (len(headers) - 1)
        count = 0
        counter = 1
        
        for row in reader:
            try:
                timestamp = datetime.strptime(row[0], '%Y-%m-%d %H:%M:%S')
                
                if current_start_time is None:
                    current_start_time = timestamp
                
                if (timestamp - current_start_time).total_seconds() < 10:
                    for i in range(1, len(headers)):
                        sums[i - 1] += float(row[i])
                    count += 1
                else:
                    avg_row = [counter] + [sums[i] / count if count > 0 else 0.0 for i in range(len(sums))]
                    writer.writerow(avg_row)
                    
                    current_start_time = timestamp
                    sums = [0.0] * (len(headers) - 1)
                    count = 0
                    
                    for i in range(1, len(headers)):
                        sums[i - 1] += float(row[i])
                    
                    count += 1
                    counter += 1
            except Exception as e:
                print(f"Error processing row {row}: {e}")
        
        if count > 0:
            avg_row = [counter] + [sums[i] / count if count > 0 else 0.0 for i in range(len(sums))]
            writer.writerow(avg_row)

calculate_10sec_average('data/cleaned/200-web_transaction_time_clean.csv', 'data/average/10-web_transaction_time_average.csv')
calculate_10sec_average('data/cleaned/200-response_time_clean.csv','data/average/10-response_time_average.csv')
