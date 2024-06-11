# MediLink_Down.py
import os
import argparse
import shutil
import glob
from MediLink_Decoder import process_file
from MediLink_DataMgmt import operate_winscp, consolidate_csvs
import MediLink_ConfigLoader
# Import decoders for other file types

"""
Main triaging function for handling report downloads and processing from various endpoints. This function
handles downloading reports, moving files, and decoding them into a readable format. The goal is to 
provide detailed receipt and troubleshooting information for the claims.

Key Enhancements:
- Handle multiple file types (ERA, 277, etc.) and integrate respective decoders.
- Support multi-endpoint processing.
- Implement progress tracking for long-running operations.
- Provide both consolidated CSV output and in-memory parsed data for real-time display.
"""
def move_downloaded_files(local_storage_path, config):
    local_response_directory = os.path.join(local_storage_path, "responses")
    
    if not os.path.exists(local_response_directory):
        os.makedirs(local_response_directory)
    
    download_dir = config['MediLink_Config']['local_storage_path']
    file_extensions = ['.era', '.277']  # Extendable list of file extensions
    
    for ext in file_extensions:
        downloaded_files = [f for f in os.listdir(download_dir) if f.endswith(ext)]
        for file in downloaded_files:
            source_path = os.path.join(download_dir, file)
            destination_path = os.path.join(local_response_directory, file)
            shutil.move(source_path, destination_path)
            MediLink_ConfigLoader.log("Moved '{}' to '{}'".format(file, local_response_directory))

def find_files(file_path_pattern):
    normalized_path = os.path.normpath(file_path_pattern)

    if "*" in normalized_path:
        matching_files = glob.glob(normalized_path)
        return [os.path.normpath(file) for file in matching_files]
    else:
        return [normalized_path] if os.path.exists(normalized_path) else []

def translate_files(files, output_directory):
    translated_files = []
    for file in files:
        try:
            process_file(file, output_directory)
            csv_file_path = os.path.join(output_directory, os.path.basename(file) + '_decoded.csv')
            MediLink_ConfigLoader.log("Translated file to CSV: {}".format(csv_file_path), level="INFO")
            translated_files.append(csv_file_path)
        except ValueError as ve:
            MediLink_ConfigLoader.log("Unsupported file type: {}".format(file), level="WARNING")
        except Exception as e:
            MediLink_ConfigLoader.log("Error processing file {}: {}".format(file, e), level="ERROR")
    
    consolidate_csv_path = consolidate_csvs(output_directory, file_prefix="Consolidated", interactive=True)
    MediLink_ConfigLoader.log("Consolidated CSV path: {}".format(consolidate_csv_path), level="INFO")
    return consolidate_csv_path, translated_files

def display_translated_files(translated_files):
    print("\nTranslated Files Summary:")
    for file in translated_files:
        print(" - {}",format(file))

def main(desired_endpoint='AVAILITY'):
    parser = argparse.ArgumentParser(description="Process files and convert them to CSV format.")
    parser.add_argument('--config_path', type=str, help='Path to the configuration JSON file', default="json/config.json")
    parser.add_argument('--desired_endpoint', type=str, help='The desired endpoint key from the configuration.', default=desired_endpoint)
    parser.add_argument('--file_path_pattern', type=str, help='Optional: Specify a path pattern for files for direct translation.', default=None)
    args = parser.parse_args()
    
    config, _ = MediLink_ConfigLoader.load_configuration(args.config_path)
    local_storage_path = config['MediLink_Config']['local_storage_path']
    output_directory = os.path.join(local_storage_path, "translated_csvs")
    
    if args.file_path_pattern:
        files = find_files(args.file_path_pattern)
        if files:
            files_str = ', '.join(files)
            MediLink_ConfigLoader.log("Translating files: {}".format(files_str), level="INFO")
            consolidate_csv_path, translated_files = translate_files(files, output_directory)
            MediLink_ConfigLoader.log("Translation and consolidation completed.", level="INFO")
            display_translated_files(translated_files)
            return consolidate_csv_path
        else:
            MediLink_ConfigLoader.log("No files found matching: {}".format(args.file_path_pattern), level="WARNING")
            return
    
    endpoint_key = args.desired_endpoint
    if endpoint_key not in config['MediLink_Config']['endpoints']:
        MediLink_ConfigLoader.log("Endpoint '{}' not found in configuration. Using default 'AVAILITY'.".format(endpoint_key), level="WARNING")
        endpoint_key = 'AVAILITY'
    
    endpoint_configs = [config['MediLink_Config']['endpoints'][key] for key in config['MediLink_Config']['endpoints']]
    downloaded_files = []

    for endpoint_config in endpoint_configs:
        downloaded_files += operate_winscp("download", None, endpoint_config, local_storage_path, config)
    
    move_downloaded_files(local_storage_path, config)
    
    # Implement progress tracking
    # from tqdm import tqdm
    # for file in tqdm(downloaded_files, desc="Translating files"):
    #     translate_files([file], output_directory)
    
    consolidate_csv_path, translated_files = translate_files(downloaded_files, output_directory)
    display_translated_files(translated_files)
    
    return consolidate_csv_path

if __name__ == "__main__":
    consolidate_csv_path = main()
    if consolidate_csv_path:
        print("CSV File Created: {}".format(consolidate_csv_path))
    else:
        print("No CSV file was created.")