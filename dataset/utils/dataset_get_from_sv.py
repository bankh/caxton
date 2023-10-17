import csv
import requests
import os
import argparse
from tqdm import tqdm

def download_files_from_tsv(source_tsv, target_folder):
    # Ensure the target folder exists or create it
    if not os.path.exists(target_folder):
        os.makedirs(target_folder)

    # Open the source TSV file and start downloading
    with open(source_tsv, 'r') as tsv_file:
        tsv_reader = csv.reader(tsv_file, delimiter=' ')
        for row in tqdm(tsv_reader):
            url = row[0]
            filename = row[1] + ".zip"
            filepath = os.path.join(target_folder, filename)
            
            response = requests.get(url, stream=True)
            with open(filepath, 'wb') as out_file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        out_file.write(chunk)

    print("All files downloaded successfully!")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download .zip files from URLs specified in a TSV.")
    parser.add_argument("source_tsv", help="Path to the source TSV file.")
    parser.add_argument("target_folder", help="Target folder to save the .zip files.")
    
    args = parser.parse_args()

    download_files_from_tsv(args.source_tsv, args.target_folder)
