import os
from datetime import datetime
import numpy as np
import torch
from pytorch_lightning import seed_everything
from torchvision import transforms

# Set the environment variable DATA_DIR
os.environ['DATA_DIR'] = '/mnt/data_drive/Data-AutoPrint'
os.environ['CUDA_VISIBLE_DEVICES'] = '0' # Pick one or multiple from the available list of GPU(s) for training '0,1,2,3,4,5,6'

DATE = datetime.now().strftime("%d%m%Y")
dataset_switch = 0
DATA_DIR = os.environ.get("DATA_DIR")

if dataset_switch == 0:
    DATASET_NAME = "dataset_single_layer"
    DATA_CSV = os.path.join(
        DATA_DIR,
        "caxton_dataset/caxton_dataset_filtered_single_extracted.csv"
        # "caxton_dataset/caxton_dataset_filtered_single.csv",
    )
    # DATASET_MEAN = [0.16853632, 0.17632364, 0.10495131]
    # DATASET_STD = [0.05298341, 0.05527821, 0.04611006]
    DATASET_MEAN = [0.41822195053100586, 0.41011959314346313, 0.3475947380065918]
    DATASET_STD = [0.3204368054866791, 0.3123301863670349, 0.339181512594223]
elif dataset_switch == 1:
    DATASET_NAME = "dataset_full"
    DATA_CSV = os.path.join(
        DATA_DIR,
        "caxton_dataset/caxton_dataset_filtered.csv",
    )
    DATASET_MEAN = [0.2915257, 0.27048784, 0.14393276]
    DATASET_STD = [0.066747, 0.06885352, 0.07679665]
elif dataset_switch == 2:
    DATASET_NAME = "dataset_equal"
    DATA_CSV = os.path.join(
        DATA_DIR,
        "caxton_dataset/caxton_dataset_filtered_equal.csv",
    )
    DATASET_MEAN = [0.2925814, 0.2713622, 0.14409496]
    DATASET_STD = [0.0680447, 0.06964592, 0.0779964]
elif dataset_switch == 3:
    DATASET_NAME = "dataset_cleaned_filtered"
    DATA_CSV = os.path.join(DATA_DIR,
                            "caxton_dataset/caxton_dataset_filtered_cleaned.csv")
    DATASET_MEAN = [0.4812980592250824, 0.4523872435092926, 0.3639879524707794]
    DATASET_STD = [0.28480225801467896, 0.27984151244163513, 0.32483652234077454]

INITIAL_LR = 0.001

BATCH_SIZE = 32 # 32 - 25% of vRAM. 160 - 95% of vRAM for MI 16GB in 16 bits of precision
MAX_EPOCHS = 100

NUM_NODES = 1
# NUM_GPUS = torch.cuda.device_count()-1
NUM_GPUS = 1
ACCELERATOR = "ddp"

def set_seed(seed):
    torch.backends.cudnn.deterministic = False
    torch.backends.cudnn.benchmark = True
    seed_everything(seed)
    torch.manual_seed(seed)
    np.random.seed(seed)

def make_dirs(path):
    try:
        os.makedirs(path)
    except:
        pass

preprocess = transforms.Compose(
    [
        transforms.Resize(224),
        transforms.ToTensor(),
        transforms.Normalize(
            [0.2915257, 0.27048784, 0.14393276],
            [0.2915257, 0.27048784, 0.14393276],
        )
    ],
)