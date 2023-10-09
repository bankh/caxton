#!/bin/bash

if [ $# -ne 1 ]; then
  echo "Usage: $0 <target_folder>"
  exit 1
fi

target_folder="$1"

# Create the target folder if it doesn't exist
mkdir -p "$target_folder"

# Create an empty array to store dataset URLs
dataset_urls=()

for ((i=0; i<192; i++)); do
    wget_link="https://www.repository.cam.ac.uk/bitstream/handle/1810/339869/print$i.zip?sequence=$((i + 7))&isAllowed=y"
    zip_file="$target_folder/print$i.zip"
    
    # Check if the zip file already exists
    if [ ! -f "$zip_file" ]; then
        wget_cmd="wget -q --show-progress -O '$zip_file' '$wget_link'"
        
        # Append the URL to the array
        dataset_urls+=("$wget_link")
        
        # Download the zip file
        eval "$wget_cmd"
    fi
done

# Save the array of dataset URLs to a CSV file
csv_file="$target_folder/dataset_list.csv"
echo "Dataset URLs" > "$csv_file"
printf "%s\n" "${dataset_urls[@]}" >> "$csv_file"

# Change to the target folder
cd "$target_folder"

# Unzip all downloaded files and check for existence before deleting
for ((i=0; i<192; i++)); do
    zip_file="print$i.zip"
    unzip_folder="print$i"
    
    if [ -f "$zip_file" ]; then
        unzip -q "$zip_file"
        
        # Check if unzip was successful before deleting the zip file
        if [ -d "$unzip_folder" ]; then
            rm "$zip_file"
        fi
    fi
done

echo "Download and unpack completed."
