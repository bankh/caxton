from pytorch_lightning.callbacks import EarlyStopping

class LoggingEarlyStopping(EarlyStopping):

    def __init__(self, logger, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logger

    def on_train_epoch_end(self, trainer, pl_module):
        super().on_train_epoch_end(trainer, pl_module)
        if self.stopped_epoch > 0:
            message = f'Early stopping occurred at epoch {self.stopped_epoch}'
            self.logger.experiment.add_text('Early Stopping', message, self.stopped_epoch)
