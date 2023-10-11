#!/bin/bash

# Check the number of arguments
if [ "$#" -ne 3 ]; then
  echo "Usage: ./script.sh <source_csv> <second_source_csv> <target_csv>"
  exit 1
fi

# Initialize variables
source_csv="$1"
second_source_csv="$2"
target_csv="$3"
declare -A print_limits

# Read the second CSV to populate the print_limits associative array
while IFS=',' read -r path part limit; do
  if [ "$path" != "Path" ]; then
    print_limits["$part"]=$limit
  fi
done < "$second_source_csv"

# Write header to target CSV
echo "img_path,timestamp,flow_rate,feed_rate,z_offset,target_hotend,hotend,bed,nozzle_tip_x,nozzle_tip_y,print_id" > "$target_csv"

# Read the source CSV line by line
while IFS=',' read -r img_path timestamp flow_rate feed_rate z_offset target_hotend hotend bed nozzle_tip_x nozzle_tip_y print_id; do
  if [ "$img_path" != "img_path" ]; then
    # Extract print and image numbers from img_path
    print_number="print${print_id}"
    image_number="${img_path##*-}"
    image_number="${image_number%%.*}"

    # Check if this row should be included in the target CSV
    if [ -n "${print_limits[$print_number]}" ] && [ "$image_number" -le "${print_limits[$print_number]}" ]; then
      echo "$img_path,$timestamp,$flow_rate,$feed_rate,$z_offset,$target_hotend,$hotend,$bed,$nozzle_tip_x,$nozzle_tip_y,$print_id" >> "$target_csv"
    fi
  fi
done < "$source_csv"
