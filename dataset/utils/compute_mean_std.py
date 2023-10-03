import torch
from torchvision import datasets, transforms
from torch.utils.data import DataLoader
import argparse

def compute_mean_std(data_dir):
    # Loading the dataset
    dataset = datasets.ImageFolder(data_dir, transform=transforms.ToTensor())
    dataloader = DataLoader(dataset, batch_size=len(dataset), shuffle=False)

    # Computing mean and standard deviation
    for images, _ in dataloader:
        # Per channel mean and standard deviation
        mean = torch.mean(images, dim=(0, 2, 3))
        std = torch.std(images, dim=(0, 2, 3))
        break  # one iteration is enough as we have loaded all data

    # Convert to list for easier readability
    mean = mean.tolist()
    std = std.tolist()

    print(f'Mean: {mean}')
    print(f'Standard Deviation: {std}')

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Compute mean and standard deviation of image dataset.')
    parser.add_argument('data_dir', type=str, help='Path to the image dataset directory.')
    args = parser.parse_args()

    compute_mean_std(args.data_dir)