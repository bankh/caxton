import csv

def calculate_average(source_csv):
    total_img_mean = 0.0
    total_img_std = 0.0
    total_rows = 0

    with open(source_csv, 'r') as f_source:
        reader = csv.reader(f_source)
        header = next(reader)  # Skip header

        for row in reader:
            img_mean = float(row[16])
            img_std = float(row[17])

            total_img_mean += img_mean
            total_img_std += img_std
            total_rows += 1

    average_img_mean = total_img_mean / total_rows
    average_img_std = total_img_std / total_rows

    print(f"Average img_mean: {average_img_mean}")
    print(f"Average img_std: {average_img_std}")

if __name__ == "__main__":
    source_csv = "/mnt/data_drive/Data-AutoPrint/caxton_dataset/caxton_dataset_filtered_single_extracted.csv"
    calculate_average(source_csv)
