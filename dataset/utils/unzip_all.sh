#!/bin/bash
# Move this bash script where the zip files are
# Make sure it is executable '$ chmod +x unzip_all.sh'
# Run the script '$./unzip_all.sh' and it will create log file in the same folder to
# crosscheck the name of the zip archive and the foldernames for potential
# inconsistencies.

# Initialize or clear the log file
> unzip_log.txt

# Loop through each zip file and unzip it
for file in *.zip; do
  echo "Unzipping $file" >> unzip_log.txt  # Log the file being unzipped
  unzip -o "$file" >> unzip_log.txt 2>&1   # Unzip the file and log the output
done
