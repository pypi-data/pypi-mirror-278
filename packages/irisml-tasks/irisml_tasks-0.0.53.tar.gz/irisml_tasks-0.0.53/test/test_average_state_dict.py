import io
import unittest

import torch
from irisml.tasks.average_state_dict import Task


class TestAverageStateDict(unittest.TestCase):
    def test_state_dicts(self):
        input_state_dicts = {'a': torch.rand(1), 'b': torch.rand((2, 3))}
        input_state_dicts2 = {'a': torch.rand(1), 'b': torch.rand((2, 3))}
        input_state_dicts3 = {'a': torch.rand(1), 'b': torch.rand((2, 3))}

        averaged_state_dict = {'a': (input_state_dicts['a'] + input_state_dicts2['a'] + input_state_dicts3['a']) / 3,
                               'b': (input_state_dicts['b'] + input_state_dicts2['b'] + input_state_dicts3['b']) / 3}
        output_state_dict = Task(Task.Config()).execute(Task.Inputs(state_dict_list=[input_state_dicts, input_state_dicts2, input_state_dicts3])).state_dict

        self.assertEqual(set(output_state_dict.keys()), {'a', 'b'})
        self.assertTrue(torch.allclose(output_state_dict['a'], averaged_state_dict['a']))
        self.assertTrue(torch.allclose(output_state_dict['b'], averaged_state_dict['b']))

        input_state_dict_bytes = self._serialize_state_dict(input_state_dicts)
        input_state_dict_bytes2 = self._serialize_state_dict(input_state_dicts2)
        input_state_dict_bytes3 = self._serialize_state_dict(input_state_dicts3)

        output_state_dict = Task(Task.Config()).execute(Task.Inputs(state_dict_bytes_list=[input_state_dict_bytes, input_state_dict_bytes2, input_state_dict_bytes3])).state_dict
        self.assertEqual(set(output_state_dict.keys()), {'a', 'b'})
        self.assertTrue(torch.allclose(output_state_dict['a'], averaged_state_dict['a']))
        self.assertTrue(torch.allclose(output_state_dict['b'], averaged_state_dict['b']))

    def test_wrong_key_set(self):
        input_state_dicts = {'a': torch.rand(1), 'b': torch.rand((2, 3))}
        missing_key = {'b': torch.rand((2, 3))}

        with self.assertRaises(ValueError):
            Task(Task.Config()).execute(Task.Inputs(state_dict_list=[input_state_dicts, missing_key]))

        extra_key = {'a': torch.rand(1), 'b': torch.rand((2, 3)), 'c': torch.rand(1)}
        with self.assertRaises(ValueError):
            Task(Task.Config()).execute(Task.Inputs(state_dict_list=[input_state_dicts, extra_key]))

    @staticmethod
    def _serialize_state_dict(state_dict):
        buffer = io.BytesIO()
        torch.save(state_dict, buffer)
        return buffer.getbuffer().tobytes()
