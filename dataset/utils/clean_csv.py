import csv
# import argparse

def remove_corrupted_images(txt_file_path, csv_file_path):
    """
    This function removes rows corresponding to corrupted images from a CSV file.
    
    Parameters:
    txt_file_path (str): The path to the text file containing the list of corrupted images.
    csv_file_path (str): The path to the CSV file from which corrupted images should be removed.
    """
    
    # Read the txt file and collect the names of corrupted images
    corrupted_images = []
    with open(txt_file_path, 'r') as txt_file:
        for line in txt_file:
            if "Skipping corrupted or incomplete image:" in line:
                corrupted_image = line.split(": ")[-1].strip().split("/")[-1]
                corrupted_images.append(corrupted_image)

    # Create a new CSV file with a '_cleaned' suffix
    new_csv_file_path = csv_file_path.replace(".csv", "_cleaned.csv")

    # Read the original CSV file and write a new one without the corrupted images
    with open(csv_file_path, 'r') as csv_file, open(new_csv_file_path, 'w', newline='') as new_csv_file:
        csv_reader = csv.reader(csv_file)
        csv_writer = csv.writer(new_csv_file)

        # Write the header
        header = next(csv_reader)
        csv_writer.writerow(header)

        for row in csv_reader:
            img_path = row[0].split("/")[-1]
            if img_path not in corrupted_images:
                csv_writer.writerow(row)

if __name__ == "__main__":
    # Hardcoded file paths
    process_txt_file_path = "/mnt/data_drive/AutoPrint/software/caxton/dataset/process_log.txt"
    csv_file_path = "/mnt/data_drive/Data-AutoPrint/caxton_dataset/caxton_dataset_filtered.csv"

    # Commented out argument parser since we're using hardcoded file paths
    # parser = argparse.ArgumentParser(description="Remove rows corresponding to corrupted images from a CSV file.")
    # parser.add_argument("--txt_file_path", type=str, help="Path to the text file.")
    # parser.add_argument("--csv_file_path", type=str, help="Path to the CSV file.")
    # args = parser.parse_args()

    # Call the function to remove corrupted images
    remove_corrupted_images(process_txt_file_path, csv_file_path)
