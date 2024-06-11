import dataclasses
import json
import logging
import pathlib
import typing
import torch
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Save a list of tensors to a JSONL file.

    Config:
        path (Path): The path to save the JSONL file.
    """
    VERSION = '0.1.0'
    CACHE_ENABLED = False

    @dataclasses.dataclass
    class Inputs:
        data: typing.List[torch.Tensor]

    @dataclasses.dataclass
    class Config:
        path: pathlib.Path

    def execute(self, inputs):
        self.config.path.parent.mkdir(parents=True, exist_ok=True)

        with self.config.path.open('w') as f:
            for item in inputs.data:
                json.dump(item.tolist(), f)
                f.write('\n')

        logger.info(f'Saved {len(inputs.data)} tensors to {self.config.path}')
        return self.Outputs()
