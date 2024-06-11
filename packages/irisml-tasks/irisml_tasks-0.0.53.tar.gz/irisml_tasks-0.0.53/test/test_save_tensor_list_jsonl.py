import pathlib
import tempfile
import unittest
import torch
from irisml.tasks.save_tensor_list_jsonl import Task


class TestSaveTensorListJsonl(unittest.TestCase):
    def test_simple(self):
        tensors = [torch.tensor([1, 2, 3]), torch.tensor([4, 5, 6])]
        with tempfile.TemporaryDirectory() as tempdir:
            path = pathlib.Path(tempdir) / 'test.jsonl'
            Task(Task.Config(path=path)).execute(Task.Inputs(data=tensors))
            lines = path.read_text().splitlines()
            self.assertEqual(len(lines), 2)
            self.assertEqual(lines[0], '[1, 2, 3]')
            self.assertEqual(lines[1], '[4, 5, 6]')
