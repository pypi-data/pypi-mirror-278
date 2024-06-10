from accelerate.tracking import GeneralTracker, on_main_process, logger, TensorBoardTracker
from accelerate.utils import listify
import time, yaml
from typing import Optional, Union
import os

class AudioTensorBoardTracker(TensorBoardTracker):
    """
    A `Tracker` class that supports `tensorboard`. Should be initialized at the start of your script.

    Args:
        run_name (`str`):
            The name of the experiment run
        logging_dir (`str`, `os.PathLike`):
            Location for TensorBoard logs to be stored.
        **kwargs (additional keyword arguments, *optional*):
            Additional key word arguments passed along to the `tensorboard.SummaryWriter.__init__` method.
    """

    @on_main_process
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @on_main_process
    def log(self, values: dict, step: Optional[int] = None, **kwargs):
        """
        Logs `values` to the current run.

        Args:
            values (Dictionary `str` to `str`, `float`, `int` or `dict` of `str` to `float`/`int`):
                Values to be logged as key-value pairs. The values need to have type `str`, `float`, `int` or `dict` of
                `str` to `float`/`int`.
            step (`int`, *optional*):
                The run step. If included, the log will be affiliated with this step.
            kwargs:
                Additional key word arguments passed along to either `SummaryWriter.add_scaler`,
                `SummaryWriter.add_text`, or `SummaryWriter.add_scalers` method based on the contents of `values`.
        """
        type = values.get('type', None)
        if type == 'figure':
            values = values['values']
            for k, v in values.items():
                self.writer.add_figure(k, v, global_step=step, **kwargs)
        elif type == 'audio':
            sample_rate = values['sample_rate']
            values = values['values']
            for k, v in values.items():
                self.writer.add_audio(k, v, global_step=step, sample_rate=sample_rate, **kwargs)
        else:
            values = listify(values)
            for k, v in values.items():
                if isinstance(v, (int, float)):
                    self.writer.add_scalar(k, v, global_step=step, **kwargs)
                elif isinstance(v, str):
                    self.writer.add_text(k, v, global_step=step, **kwargs)
                elif isinstance(v, dict):
                    self.writer.add_scalars(k, v, global_step=step, **kwargs)
        self.writer.flush()
        logger.debug("Successfully logged to TensorBoard")

    # @on_main_process
    # def log_images(self, values: dict, step: Optional[int], **kwargs):
    #     """
    #     Logs `images` to the current run.

    #     Args:
    #         values (Dictionary `str` to `List` of `np.ndarray` or `PIL.Image`):
    #             Values to be logged as key-value pairs. The values need to have type `List` of `np.ndarray` or
    #         step (`int`, *optional*):
    #             The run step. If included, the log will be affiliated with this step.
    #         kwargs:
    #             Additional key word arguments passed along to the `SummaryWriter.add_image` method.
    #     """
    #     for k, v in values.items():
    #         self.writer.add_images(k, v, global_step=step, **kwargs)
    #     logger.debug("Successfully logged images to TensorBoard")
        
            
    # @on_main_process
    # def log_audios(self, values: dict, step: Optional[int], sample_rate=16000, **kwargs):
        
    #     for k, v in values.items():
    #         self.writer.add_audio(k, v, global_step=step, sample_rate=sample_rate, **kwargs)
    #     logger.debug("Successfully logged audios to TensorBoard")

    # @on_main_process
    # def finish(self):
    #     """
    #     Closes `TensorBoard` writer
    #     """
    #     self.writer.close()
    #     logger.debug("TensorBoard writer closed")