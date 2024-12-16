import csv
from datetime import datetime

input_file_paths = ['tests/microservice/200-micro_load_test.csv', 'tests/microservice/200-mono_load_test.csv', 'tests/microservice/200-hybrid_load_test.csv', 'tests/microservice/200-dist_micro_load_test.csv', 'tests/microservice/200-dist_mono_load_test.csv', 'tests/microservice/200-dist_hybrid_load_test.csv']

response_time_output_file_path = 'data/cleaned/200-response_time_clean.csv'
web_transaction_time_output_file_path = 'data/cleaned/200-web_transaction_time_clean.csv'

col_web_transaction_time = ['http_req_blocked', 'http_req_connecting', 'http_req_tls_handshaking', 'http_req_sending', 'http_req_waiting', 'http_req_receiving']

data = [
    ['timestamp', 'micro_response_time', 'micro_web_transaction_time', 'micro_vus', 'mono_response_time', 'mono_web_transaction_time', 'mono_vus', 'hybrid_response_time', 'hybrid_web_transaction_time', 'hybrid_vus']
]

response_time_data = [
    ['timestamp', 'micro_response_time', 'micro_vus', 'mono_response_time', 'mono_vus', 'hybrid_response_time', 'hybrid_vus', 'dist_micro_response_time', 'dist_micro_vus', 'dist_mono_response_time', 'dist_mono_vus', 'dist_hybrid_response_time', 'dist_hybrid_vus']
]

web_transaction_time_data = [
    ['timestamp', 'micro_web_transaction_time', 'micro_vus', 'mono_web_transaction_time', 'mono_vus', 'hybrid_web_transaction_time', 'hybrid_vus', 'dist_micro_web_transaction_time', 'dist_micro_vus', 'dist_mono_web_transaction_time', 'dist_mono_vus', 'dist_hybrid_web_transaction_time', 'dist_hybrid_vus']
]

def process_csv(input_file_path, idx):
    with open(input_file_path, mode='r') as file:
        csv_reader = csv.reader(file)

        counter = 1
        web_transaction_time = 0
        http_req_duration = 0
        
        for row in csv_reader:
            timestamp = datetime.fromtimestamp(int(row[1])).strftime('%Y-%m-%d %H:%M:%S')
            
            if row[0] in col_web_transaction_time:
                web_transaction_time += float(row[2])
            elif row[0] == 'http_req_duration':
                http_req_duration = float(row[2])
            elif row[0] == 'vus':
                vus = float(row[2])
                if idx == 0:
                    response_time_data.append([timestamp, http_req_duration, vus])
                    web_transaction_time_data.append([datetime.fromtimestamp(int(row[1])).strftime('%Y-%m-%d %H:%M:%S'), web_transaction_time, vus])
                else:
                    try:
                        response_time_data[counter].extend([http_req_duration, vus])
                        web_transaction_time_data[counter].extend([web_transaction_time, vus])
                    except IndexError as e:
                        print(e)

                web_transaction_time = 0
                counter += 1


for idx, input_file_path in enumerate(input_file_paths):
    process_csv(input_file_path, idx)
    print(f'Processing {input_file_path.split('/')[-1]}')
    

with open(response_time_output_file_path, mode='w', newline='', encoding='utf-8') as file:
    csv_writer = csv.writer(file)
    
    csv_writer.writerows(response_time_data)
    
with open(web_transaction_time_output_file_path, mode='w', newline='', encoding='utf-8') as file:
    csv_writer = csv.writer(file)
    
    csv_writer.writerows(web_transaction_time_data)
    