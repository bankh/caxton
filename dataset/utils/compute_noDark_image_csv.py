"""
This script filters a CSV file to remove rows based on the average image brightness.
Rows with an 'img_mean' value below a specified threshold will be excluded.
The filtered data is then saved to a new CSV file.
"""

# Import necessary libraries
import sys
import os

# Environment Check
print("Running Python version:", sys.version)
print("Current working directory:", os.getcwd())

# Ensure pandas is installed
try:
    import pandas as pd
except ImportError as e:
    sys.exit("Error: pandas library is not installed. Please install it using 'pip install pandas'.")


def filter_dark_images(csv_file, output_file, threshold=10):
    # Read the CSV file into a DataFrame
    df = pd.read_csv(csv_file)

    # Filter out rows where img_mean is less than the threshold
    filtered_df = df[df['img_mean'] >= threshold]

    # Save the filtered DataFrame to a new CSV file
    filtered_df.to_csv(output_file, index=False)

# File paths
#csv_file = 'path_to_your_csv_file.csv'  # replace with your CSV file path
csv_file = '/caxton_dataset/caxton_dataset_filtered_no_outliers_img_info.csv'
output_file = '/caxton_dataset_filtered_no_outliers_img_info_NoDark.csv'

# Call the function
filter_dark_images(csv_file, output_file)
print(f"Filtered CSV file saved as: {output_file}")
