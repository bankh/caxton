import os
import argparse

import pytorch_lightning as pl
from pytorch_lightning import loggers as pl_loggers
from pytorch_lightning.callbacks import ModelCheckpoint

from data.data_module import ParametersDataModule
from model.network_module import ParametersClassifier
from utils.early_stopping import LoggingEarlyStopping
from train_config import *

parser = argparse.ArgumentParser()
parser.add_argument(
    "-s", 
    "--seed", 
    default=12, 
    type=int, 
    help="Set seed for training"
)
parser.add_argument(
    "-e",
    "--epochs",
    default=MAX_EPOCHS,
    type=int,
    help="Number of epochs to train the model for",
)
parser.add_argument(
    "-c",
    "--checkpoint",
    default=False,
    type=bool,
    help="On/ off the checkpoint and make sure to enter ckpt_filename inside the code",
)
args = parser.parse_args()
seed = args.seed
set_seed(seed)

logs_dir = "logs/logs-{}/{}/".format(DATE, seed)
logs_dir_default = os.path.join(logs_dir, "default")
# Create directories
os.makedirs(logs_dir, exist_ok=True)
os.makedirs(logs_dir_default, exist_ok=True)

tb_logger = pl_loggers.TensorBoardLogger(save_dir=logs_dir, name='lightning_logs')
dirpath = "checkpoints/{}/{}/".format(DATE, seed)
filename = "MHResAttNet-{}-{}-".format(DATASET_NAME, DATE) + "{epoch:02d}-{val_loss:.2f}-{val_acc:.2f}"
ckpt_filename = ("/mnt/data_drive/AutoPrint/software/caxton/checkpoints/03102023/1234/"
                 "MHResAttNet-dataset_full-03102023-epoch=18-val_loss=4.10-val_acc=0.48.ckpt")
checkpoint_path = os.path.join(dirpath, ckpt_filename)
checkpoint_callback = ModelCheckpoint(
    monitor="val_loss",
    dirpath=dirpath,
    filename=filename,
    save_top_k=3,
    mode="max",
)
early_stop_callback = LoggingEarlyStopping(logger=tb_logger,
                                           monitor='val_loss', 
                                           patience=100,
                                           verbose=True,
                                           mode='min'
)
model = ParametersClassifier(num_classes=3, #classes:low,good,high|labels:flowrate,lateralspeed,Zoffset,hotendtemperature
                             lr=INITIAL_LR,
                             gpus=NUM_GPUS,
                             transfer=False,
)
data = ParametersDataModule(batch_size=BATCH_SIZE,
                            data_dir=DATA_DIR,
                            csv_file=DATA_CSV,
                            dataset_name=DATASET_NAME,
                            mean=DATASET_MEAN,
                            std=DATASET_STD,
)
trainer = pl.Trainer(num_nodes=NUM_NODES,
                    #  gpus=NUM_GPUS,
                     devices=NUM_GPUS,
                     accelerator='gpu',
                     strategy=ACCELERATOR,
                     max_epochs=args.epochs,
                     logger=tb_logger,
                     enable_model_summary=None,
                     precision=32,
                     callbacks=[checkpoint_callback, early_stop_callback],
                     resume_from_checkpoint=checkpoint_path if args.checkpoint else None,  
)
trainer.fit(model, data)
