from typing import Any, Dict, List, Optional, Tuple

from transformers import pipeline

from ..utils import normalize_model_output


class FillMaskTransformation:
    """
    Fill Mask Transformation

    Input Format: <str>
        Examples: "Sample sentence <mask_placeholder>", "Sample sentence [MASK]"
    Output Format: [{'score': <float>, 'token': <int>, 'token_str': <str>}, ...]
    """

    def __init__(self, model: str, input_field: str, output_field: str,
                 mask_placeholder: str = '[MASK]',
                 mask_targets: Optional[List[str]] = None,
                 top_k_scores: Optional[int] = 5,
                 gpu_device: Optional[int] = None,
                 batch_size: Optional[int] = None):
        self._model = model
        self._input_field = input_field
        self._output_field = output_field
        self._mask_placeholder = mask_placeholder
        self._mask_targets = mask_targets
        self._top_k_scores = top_k_scores if top_k_scores else 5
        self._gpu_device = gpu_device
        extra_args = {}
        if batch_size:
            extra_args['batch_size'] = batch_size
        self._pipeline = pipeline(model=self._model, device=self._gpu_device,
                                  top_k=self._top_k_scores,
                                  task='fill-mask',
                                  **extra_args)

    def transform(self, data_list: List[Dict[str, Any]]):
        indexed_inputs = self._get_indexed_inputs(data_list)
        model_inputs = [d for _, d in indexed_inputs]
        if not model_inputs:
            return
        if self._mask_placeholder != '[MASK]':
            model_inputs = [str(d).replace(self._mask_placeholder, '[MASK]') for d in model_inputs]
        if self._mask_targets:
            model_outputs = self._pipeline(model_inputs, targets=self._mask_targets)
        else:
            model_outputs = self._pipeline(model_inputs)
        model_outputs = normalize_model_output(model_outputs)
        self._set_all_scores(data_list, indexed_inputs, model_outputs)

    def _get_indexed_inputs(self, data_list: List[Dict[str, Any]]) -> List[Tuple[int, str]]:
        indexed_inputs = []
        for idx, data in enumerate(data_list):
            if self._input_field in data and data[self._input_field] is not None:
                indexed_inputs.append((idx, data[self._input_field],))

        return indexed_inputs

    def _set_all_scores(self, data_list: List[Dict[str, Any]], indexed_inputs: List[Tuple[int, str]],
                        model_outputs: List[List[Dict]]):
        for idx, (data_index, _) in enumerate(indexed_inputs):
            model_output = model_outputs[idx]
            model_output = [FillMaskTransformation._remove_sequence(d) for d in model_output]
            data_list[data_index][self._output_field] = model_output

    @staticmethod
    def _remove_sequence(output: dict):
        if 'sequence' in output:
            output.pop('sequence')
        return output
