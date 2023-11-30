# # import csv

# # def calculate_average(source_csv):
# #     total_img_mean = 0.0
# #     total_img_std = 0.0
# #     total_rows = 0

# #     with open(source_csv, 'r') as f_source:
# #         reader = csv.reader(f_source)
# #         header = next(reader)  # Skip header

# #         for row in reader:
# #             img_mean = float(row[16])
# #             img_std = float(row[17])

# #             total_img_mean += img_mean
# #             total_img_std += img_std
# #             total_rows += 1

# #     average_img_mean = total_img_mean / total_rows
# #     average_img_std = total_img_std / total_rows

# #     print(f"Average img_mean: {average_img_mean}")
# #     print(f"Average img_std: {average_img_std}")

# # if __name__ == "__main__":
# #     source_csv = "/mnt/data_drive/Data-AutoPrint/caxton_dataset/caxton_dataset_filtered_single_extracted.csv"
# #     calculate_average(source_csv)
# import csv
# import torch
# from torchvision import transforms
# from PIL import Image
# import numpy as np
# import os
# from tqdm import tqdm

# def calculate_mean_std(csv_file):
#     transform = transforms.Compose([
#         transforms.Resize((224, 224)),
#         transforms.ToTensor()
#     ])
    
#     means = []
#     stds = []
#     csv_dir = os.path.dirname(csv_file)

#     with open(csv_file, 'r') as f:
#         reader = csv.DictReader(f)
#         for row in tqdm(reader, desc="Processing"):
#             try:
#                 # Construct the full image path
#                 # Remove the first directory from the img_path
#                 img_relative_path_parts = row['img_path'].split(os.sep)[1:]  # Split and remove the first part
#                 img_relative_path = os.path.join(*img_relative_path_parts)  # Reconstruct the path without the first directory
#                 img_path = os.path.join(csv_dir, img_relative_path)
#                 img = Image.open(img_path).convert('RGB')
#                 img_t = transform(img)
#                 means.append(torch.mean(img_t, dim=(1,2)).numpy())
#                 stds.append(torch.std(img_t, dim=(1,2)).numpy())
#             except OSError as e:
#                 print(f"Skipping corrupted image file: {img_path}")
#                 continue

#     mean = np.array(means).mean(axis=0)
#     std = np.array(stds).mean(axis=0)

#     return mean, std

# # Replace with your actual CSV path
# csv_file = '/mnt/data_drive/Data-AutoPrint/caxton_dataset/caxton_dataset_filtered.csv'  # Update this path to the CSV file location
# mean, std = calculate_mean_std(csv_file)
# print(f"Mean: {mean}")
# print(f"Std: {std}")

import torch
from torchvision import transforms
from torch.utils.data import DataLoader, Dataset
import pandas as pd
from wand.image import Image
from skimage import io
import numpy as np

class ImageDatasetFromCSV(Dataset):
    def __init__(self, csv_file, transform=None):
        self.dataframe = pd.read_csv(csv_file)
        self.transform = transform

    def __len__(self):
        return len(self.dataframe)

    def __getitem__(self, idx):
        img_name = '/mnt/data_drive/Data-AutoPrint/' + self.dataframe.iloc[idx, 0]
        try:
            with Image(filename=img_name) as img:
                image = np.array(img)
                if self.transform:
                    image = self.transform(image)
        except Exception as e:
            print(f"Error opening image {img_name}: {e}")
            return None  # Returning None for errored images

        return image

def custom_collate_fn(batch):
    batch = [data for data in batch if data is not None]
    return torch.utils.data.dataloader.default_collate(batch)

def calculate_mean_std(csv_file, batch_size=1000, num_workers=16):
    transform = transforms.Compose([transforms.ToTensor()])
    dataset = ImageDatasetFromCSV(csv_file, 
                                  transform=transform)
    loader = DataLoader(dataset, 
                        batch_size=batch_size, 
                        shuffle=False, 
                        num_workers=num_workers,
                        collate_fn=custom_collate_fn)

    sum, sum_squared, num_batches = 0, 0, 0
    total_batches = len(loader)
    for i, data in enumerate(loader):
        if data is not None and len(data) > 0:
            # Calculate mean and mean squared per batch
            sum += torch.mean(data, dim=[0, 2, 3])
            sum_squared += torch.mean(data ** 2, dim=[0, 2, 3])
            num_batches += 1

        # Print the progress
        progress = (i + 1) / total_batches * 100
        print(f"Processing batch {i+1}/{total_batches} ({progress:.2f}%)")


    # Compute mean and standard deviation
    mean = sum / num_batches
    std = (sum_squared / num_batches - mean ** 2) ** 0.5

    return mean, std

# CSV file with image paths
csv_file = '/mnt/data_drive/Data-AutoPrint/caxton_dataset/caxton_dataset_filtered.csv'

# Call the function
mean, std = calculate_mean_std(csv_file, batch_size=100, num_workers=4)
print(f"Mean: {mean}")
print(f"Std: {std}")

