import torch
from torchvision import transforms
from PIL import Image
import argparse
import os
import csv

def compute_mean_std(data_dir, target_csv, batch_size=100):
    all_means = []
    all_stds = []
    
    filepath = os.path.join(target_csv)
    csv_filename = os.path.basename(target_csv).split('.')[0]
    
    with open(f'./dataset/process_{csv_filename}.txt', 'a') as log_file:
        log_file.write(f"Processing {filepath}...\n")
        print(f"Processing {filepath}...")
        
        total_images = sum(1 for row in csv.reader(open(filepath))) - 1
        processed_images = 0
        image_batch = []
        
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                img_path = os.path.join(data_dir, row['img_path'])
                try:
                    if os.path.exists(img_path):
                        processed_images += 1
                        parent_folder = os.path.basename(os.path.dirname(row['img_path']))
                        filename = os.path.basename(row['img_path'])
                        log_message = f"Processing {parent_folder}/{filename} (image {processed_images} out of {total_images})"
                        log_file.write(log_message + '\n')
                        print(log_message)
                        
                        image = Image.open(img_path).convert('RGB')
                        image = transforms.ToTensor()(image)
                        image_batch.append(image)
                        
                        if len(image_batch) == batch_size:
                            image_tensor = torch.stack(image_batch)
                            mean = torch.mean(image_tensor, dim=(0, 2, 3))
                            std = torch.std(image_tensor, dim=(0, 2, 3))
                            all_means.append(mean)
                            all_stds.append(std)
                            image_batch = []
                            
                except OSError:
                    error_message = f"Skipping corrupted or incomplete image: {img_path}"
                    log_file.write(error_message + '\n')
                    print(error_message)
        
        if image_batch:
            image_tensor = torch.stack(image_batch)
            mean = torch.mean(image_tensor, dim=(0, 2, 3))
            std = torch.std(image_tensor, dim=(0, 2, 3))
            all_means.append(mean)
            all_stds.append(std)
        
        overall_mean = torch.stack(all_means).mean(dim=0)
        overall_std = torch.stack(all_stds).mean(dim=0)
        
        log_file.write(f"Mean: {overall_mean.tolist()}\n")
        log_file.write(f"Standard Deviation: {overall_std.tolist()}\n")
        print(f"Mean: {overall_mean.tolist()}")
        print(f"Standard Deviation: {overall_std.tolist()}")

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description='Compute mean and standard deviation of image dataset based on a target CSV.')
    # parser.add_argument('data_dir', type=str, help='Path to the image dataset directory.')
    # parser.add_argument('target_csv', type=str, help='Path to the target CSV file.')
    # args = parser.parse_args()
    
    # compute_mean_std(args.data_dir, args.target_csv)

    # Hardcode the directories for debugging
    data_dir = "/mnt/data_drive/Data-AutoPrint"
    csv_dir = "/mnt/data_drive/Data-AutoPrint/caxton_dataset/caxton_dataset_filtered_cleaned.csv"
    
    compute_mean_std(data_dir, csv_dir)