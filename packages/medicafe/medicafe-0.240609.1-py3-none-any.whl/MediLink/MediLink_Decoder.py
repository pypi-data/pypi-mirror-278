# MediLink_Decoder.py
import os
import sys
import csv
from MediLink_ConfigLoader import load_configuration, log
from MediLink_Parser import parse_era_content, parse_277_content

def process_file(file_path, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    file_type = determine_file_type(file_path)
    content = read_file(file_path)
    
    if file_type == 'ERA':
        records = parse_era_content(content)
        fieldnames = ['Date of Service', 'Check EFT', 'Chart Number', 'Payer Address', 'Amount Paid', 
                      'Adjustment Amount', 'Allowed Amount', 'Write Off', 'Patient Responsibility', 'Charge']
    elif file_type == '277':
        records = parse_277_content(content)
        fieldnames = ['Clearing House', 'Received Date', 'Claim Status Tracking #', 'Billed Amt', 'Date of Service', 
                      'Last', 'First', 'Acknowledged Amt', 'Status']
    else:
        raise ValueError("Unsupported file type: {}".format(file_type))

    output_file_path = os.path.join(output_directory, os.path.basename(file_path) + '_decoded.csv')
    write_records_to_csv(records, output_file_path, fieldnames)
    print("Decoded data written to {}".format(output_file_path))

def determine_file_type(file_path):
    if file_path.endswith('.era'):
        return 'ERA'
    elif file_path.endswith('.277'):
        return '277'
    else:
        raise ValueError("Unsupported file type for file: {}".format(file_path))
    
def read_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read().replace('\n', '')
    return content

def write_records_to_csv(records, output_file_path, fieldnames):
    with open(output_file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for record in records:
            writer.writerow(record)

if __name__ == "__main__":
    config = load_configuration()
    
    files = sys.argv[1:]
    if not files:
        log("No files provided as arguments.", 'error')
        sys.exit(1)

    output_directory = config['output_directory']
    for file_path in files:
        try:
            process_file(file_path, output_directory)
        except Exception as e:
            log("Failed to process {}: {}".format(file_path, e), 'error')