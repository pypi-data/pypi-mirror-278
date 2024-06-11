import dataclasses
import logging
import irisml.core

logger = logging.getLogger(__name__)


class Task(irisml.core.TaskBase):
    """Create a list from input objects.

    This is a work around for the lack of support for list inputs in IrisML.
    """
    VERSION = '0.1.0'

    @dataclasses.dataclass
    class Inputs:
        input_dict0: dict | None = None
        input_dict1: dict | None = None
        input_dict2: dict | None = None
        input_dict3: dict | None = None
        input_dict4: dict | None = None
        input_bytes0: bytes | None = None
        input_bytes1: bytes | None = None
        input_bytes2: bytes | None = None
        input_bytes3: bytes | None = None
        input_bytes4: bytes | None = None

    @dataclasses.dataclass
    class Outputs:
        list_dict: list[dict] | None = None
        list_bytes: list[bytes] | None = None

    def execute(self, inputs):
        input_dicts = [inputs.input_dict0, inputs.input_dict1, inputs.input_dict2, inputs.input_dict3, inputs.input_dict4]
        input_bytes = [inputs.input_bytes0, inputs.input_bytes1, inputs.input_bytes2, inputs.input_bytes3, inputs.input_bytes4]

        if any(d is not None for d in input_dicts) and any(b is not None for b in input_bytes):
            raise ValueError("Only one type of input can be provided")

        result = [d for d in input_dicts if d is not None]
        if result:
            logger.info(f"Created a list of dictionaries with {len(result)} elements")
            return self.Outputs(list_dict=result)

        result = [b for b in input_bytes if b is not None]
        if result:
            logger.info(f"Created a list of bytes with {len(result)} elements")
            return self.Outputs(list_bytes=result)

        raise ValueError("At least one input must be provided")

    def dry_run(self, inputs):
        return self.execute(inputs)
