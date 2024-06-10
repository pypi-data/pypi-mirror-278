from typing import Any, Dict, List, Optional, Tuple

from transformers import pipeline

from ..utils import normalize_model_output


class TextClassificationTransformation:
    """
    Text Classification Transformation

    Input Format: <str>
    Output Format: [{'label': <str>, 'score': <float>}, ...]
    """

    def __init__(self, model: str, input_field: str, output_field: str,
                 gpu_device: Optional[int] = None):
        self._model = model
        self._input_field = input_field
        self._output_field = output_field
        self._gpu_device = gpu_device
        self._pipeline = pipeline(model=self._model, device=self._gpu_device,
                                  top_k=None,
                                  task='text-classification')

    def transform(self, data_list: List[Dict[str, Any]]):
        indexed_inputs = self._get_indexed_inputs(data_list)
        model_inputs = [d for _, d in indexed_inputs]
        if not model_inputs:
            return
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
            data_list[data_index][self._output_field] = model_output
