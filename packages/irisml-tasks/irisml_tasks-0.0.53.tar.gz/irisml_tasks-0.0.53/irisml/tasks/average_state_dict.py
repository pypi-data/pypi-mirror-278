import dataclasses
import io
import logging
import torch
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Average a list of state_dicts.

    This task accepts a list of state dict objects or a list of bytes objects that is a serialized state_dict.

    All state_dicts must have the same keys.
    """
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Inputs:
        state_dict_list: list[dict] | None = None
        state_dict_bytes_list: list[bytes] | None = None

    @dataclasses.dataclass
    class Outputs:
        state_dict: dict

    def execute(self, inputs):
        num_sources = len([x for x in [inputs.state_dict_list, inputs.state_dict_bytes_list] if x])
        if num_sources != 1:
            raise ValueError("One state_dict source must be provided.")

        state_dict_list = None
        if inputs.state_dict_list:
            state_dict_list = inputs.state_dict_list
        if inputs.state_dict_bytes_list:
            state_dict_list = [torch.load(io.BytesIO(x), map_location='cpu') for x in inputs.state_dict_bytes_list]

        assert state_dict_list, "Failed to load the state_dict."

        logger.info(f"Loaded {len(state_dict_list)} state_dicts.")

        # Verify the key names
        key_names = [set(x.keys()) for x in state_dict_list]
        for i in range(1, len(key_names)):
            extra_keys = key_names[i] - key_names[0]
            if extra_keys:
                raise ValueError(f"State dict {i} has extra keys: {extra_keys}")
            missing_keys = key_names[0] - key_names[i]
            if missing_keys:
                raise ValueError(f"State dict {i} is missing keys: {missing_keys}")

        state_dict = {}
        for k in state_dict_list[0].keys():
            state_dict[k] = sum([x[k] for x in state_dict_list]) / len(state_dict_list)

        return self.Outputs(state_dict=state_dict)

    def dry_run(self, inputs):
        return self.execute(inputs)
