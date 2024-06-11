from typing import Any, Dict, List, Optional, Tuple

from transformers import pipeline, set_seed

from ..utils import normalize_model_output


class TextGenerationTransformation:
    """
    Text Generation Transformation

    Input Format: <str>
    Output Format: <str>
    """

    def __init__(self, model: str, input_field: str, output_field: str,
                 max_length: Optional[int] = None,
                 max_new_tokens: Optional[int] = None,
                 min_length: Optional[int] = None,
                 min_new_tokens: Optional[int] = None,
                 do_sample: Optional[bool] = False,
                 num_beams: Optional[int] = 1,
                 temperature: Optional[float] = 1.0,
                 top_k: Optional[int] = 50,
                 gpu_device: Optional[int] = None,
                 batch_size: Optional[int] = None):
        self._model = model
        self._input_field = input_field
        self._output_field = output_field
        self._gpu_device = gpu_device
        extra_args = {}
        if batch_size:
            extra_args['batch_size'] = batch_size
        model_kwargs = {}
        if max_length:
            model_kwargs['max_length'] = max_length,
        if max_new_tokens:
            model_kwargs['max_new_tokens'] = max_new_tokens
        if min_length:
            model_kwargs['min_length'] = min_length
        if min_new_tokens:
            model_kwargs['min_new_tokens'] = min_new_tokens
        model_kwargs['do_sample'] = True if do_sample else False
        model_kwargs['num_beams'] = num_beams if num_beams else 1
        model_kwargs['temperature'] = float(temperature) if temperature else 1.0
        model_kwargs['top_k'] = top_k if top_k else 50
        set_seed(0)  # setting globally; might conflict with other models
        self._pipeline = pipeline(model=self._model, device=self._gpu_device,
                                  task='text-generation',
                                  **extra_args,
                                  **model_kwargs)

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
                        model_outputs: List[List[Dict[str, str]]]):
        for idx, (data_index, _) in enumerate(indexed_inputs):
            model_output = model_outputs[idx][0]
            data_list[data_index][self._output_field] = model_output.get('generated_text', '')
