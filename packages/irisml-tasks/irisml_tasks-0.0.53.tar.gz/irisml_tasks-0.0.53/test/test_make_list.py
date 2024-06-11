import unittest
from irisml.tasks.make_list import Task


class TestMakeList(unittest.TestCase):
    def test_dict(self):
        dict0 = {'a': 1}
        dict1 = {'b': 2}
        dict2 = {'c': 3}

        outputs = Task(Task.Config()).execute(Task.Inputs(input_dict0=dict0, input_dict1=dict1, input_dict2=dict2))
        self.assertEqual(outputs.list_dict, [dict0, dict1, dict2])

    def test_bytes(self):
        bytes0 = b'abc'
        bytes1 = b'def'
        bytes2 = b'ghi'

        outputs = Task(Task.Config()).execute(Task.Inputs(input_bytes0=bytes0, input_bytes1=bytes1, input_bytes2=bytes2))
        self.assertEqual(outputs.list_bytes, [bytes0, bytes1, bytes2])

    def test_multiple_inputs(self):
        with self.assertRaises(ValueError):
            Task(Task.Config()).execute(Task.Inputs(input_dict0={'a': 3}, input_bytes0=b''))

    def test_empty(self):
        with self.assertRaises(ValueError):
            Task(Task.Config()).execute(Task.Inputs())
