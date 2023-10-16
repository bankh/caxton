#!/bin/bash

# Check if both arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <source_csv> <target_folder>"
    exit 1
fi

source_csv="$1"
target_folder="$2"

# Create the target folder if it doesn't exist
mkdir -p "$target_folder"

# Read the CSV line by line
while IFS=, read -r url filename; do
    # Check if the file has a .zip extension
    if [[ "$filename" == *.zip ]]; then
        echo "Downloading $filename..."
        curl -o "$target_folder/$filename" "$url"
    fi
done < "$source_csv"

echo "Download complete!"

