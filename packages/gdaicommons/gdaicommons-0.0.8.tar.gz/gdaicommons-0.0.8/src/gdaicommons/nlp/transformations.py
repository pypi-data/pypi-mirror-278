from gdtransform.transform import transformation_builder

from .fill_mask import FillMaskTransformation
from .text2text_generation import Text2TextGenerationTransformation
from .text_classification import TextClassificationTransformation
from .text_generation import TextGenerationTransformation
from .text_labelling import TextLabellingTransformation
from .text_summarization import TextSummarizationTransformation
from ..constants import VALUE_SEPARATOR
from ..utils import blank_if_null, parse_parameter


@transformation_builder(name='text-classification-builder', is_batch=True)
def text_classification(*args, **kwargs):
    model = kwargs['model']
    input_field = kwargs['input_field']
    output_field = kwargs['output_field']
    gpu_device = int(kwargs.get('gpu_device')) if 'gpu_device' in kwargs and kwargs['gpu_device'] else None

    text_classifier = TextClassificationTransformation(model, input_field, output_field,
                                                       gpu_device=gpu_device)

    return text_classifier.transform


@transformation_builder(name='text-labelling-builder', is_batch=True)
def text_labelling(*args, **kwargs):
    model = kwargs['model']
    input_field = kwargs['input_field']
    output_field = kwargs['output_field']
    labels = kwargs['labels']
    labels = str(labels).split(sep=VALUE_SEPARATOR)
    labels = [l.strip() for l in labels]
    gpu_device = int(kwargs.get('gpu_device')) if 'gpu_device' in kwargs and kwargs['gpu_device'] else None

    text_labeller = TextLabellingTransformation(model, input_field, output_field, labels,
                                                gpu_device=gpu_device)
    return text_labeller.transform


@transformation_builder(name='fill-mask-builder', is_batch=True)
def fill_mask(*args, **kwargs):
    model = kwargs['model']
    input_field = kwargs['input_field']
    output_field = kwargs['output_field']
    mask_placeholder = kwargs.get('mask_placeholder', '[MASK]')
    mask_targets = kwargs.get('mask_targets', None)
    if mask_targets:
        mask_targets = str(mask_targets).split(sep=VALUE_SEPARATOR)
        mask_targets = [t.strip() for t in mask_targets]
    gpu_device = int(kwargs.get('gpu_device')) if 'gpu_device' in kwargs and kwargs['gpu_device'] else None

    fill_mask_transformation = FillMaskTransformation(model, input_field, output_field,
                                                      mask_placeholder=mask_placeholder,
                                                      mask_targets=mask_targets,
                                                      top_k_scores=5,
                                                      gpu_device=gpu_device)
    return fill_mask_transformation.transform


@transformation_builder(name='text-generation-builder', is_batch=True)
def text_generation(*args, **kwargs):
    model = kwargs['model']
    input_field = kwargs['input_field']
    output_field = kwargs['output_field']
    max_length = parse_parameter(kwargs.get('max_length', None), int)
    max_new_tokens = parse_parameter(kwargs.get('max_new_tokens', None), int)
    min_length = parse_parameter(kwargs.get('min_length', None), int)
    min_new_tokens = parse_parameter(kwargs.get('min_new_tokens', None), int)
    do_sample = blank_if_null(kwargs.get('do_sample', 'false')).lower() in ['true']
    num_beams = parse_parameter(kwargs.get('num_beams', '1'), int)
    temperature = parse_parameter(kwargs.get('temperature', '1.0'), float)
    top_k = parse_parameter(kwargs.get('top_k', '50'), int)
    gpu_device = int(kwargs.get('gpu_device')) if 'gpu_device' in kwargs and kwargs['gpu_device'] else None

    text_generation_transformation = TextGenerationTransformation(model, input_field, output_field,
                                                                  max_length=max_length,
                                                                  max_new_tokens=max_new_tokens,
                                                                  min_length=min_length,
                                                                  min_new_tokens=min_new_tokens,
                                                                  do_sample=do_sample,
                                                                  num_beams=num_beams,
                                                                  temperature=temperature,
                                                                  top_k=top_k,
                                                                  gpu_device=gpu_device)
    return text_generation_transformation.transform


@transformation_builder(name='text-summarization-builder', is_batch=True)
def text_summarization(*args, **kwargs):
    model = kwargs['model']
    input_field = kwargs['input_field']
    output_field = kwargs['output_field']
    max_length = parse_parameter(kwargs.get('max_length', None), int)
    max_new_tokens = parse_parameter(kwargs.get('max_new_tokens', None), int)
    min_length = parse_parameter(kwargs.get('min_length', None), int)
    min_new_tokens = parse_parameter(kwargs.get('min_new_tokens', None), int)
    do_sample = blank_if_null(kwargs.get('do_sample', 'false')).lower() in ['true']
    num_beams = parse_parameter(kwargs.get('num_beams', '1'), int)
    temperature = parse_parameter(kwargs.get('temperature', '1.0'), float)
    top_k = parse_parameter(kwargs.get('top_k', '50'), int)
    gpu_device = int(kwargs.get('gpu_device')) if 'gpu_device' in kwargs and kwargs['gpu_device'] else None

    text_summarization_transformation = TextSummarizationTransformation(model, input_field, output_field,
                                                                        max_length=max_length,
                                                                        max_new_tokens=max_new_tokens,
                                                                        min_length=min_length,
                                                                        min_new_tokens=min_new_tokens,
                                                                        do_sample=do_sample,
                                                                        num_beams=num_beams,
                                                                        temperature=temperature,
                                                                        top_k=top_k,
                                                                        gpu_device=gpu_device)
    return text_summarization_transformation.transform


@transformation_builder(name='text2text-generation-builder', is_batch=True)
def text2text_generation(*args, **kwargs):
    model = kwargs['model']
    input_field = kwargs['input_field']
    output_field = kwargs['output_field']
    max_length = parse_parameter(kwargs.get('max_length', None), int)
    max_new_tokens = parse_parameter(kwargs.get('max_new_tokens', None), int)
    min_length = parse_parameter(kwargs.get('min_length', None), int)
    min_new_tokens = parse_parameter(kwargs.get('min_new_tokens', None), int)
    do_sample = blank_if_null(kwargs.get('do_sample', 'false')).lower() in ['true']
    num_beams = parse_parameter(kwargs.get('num_beams', '1'), int)
    temperature = parse_parameter(kwargs.get('temperature', '1.0'), float)
    top_k = parse_parameter(kwargs.get('top_k', '50'), int)
    gpu_device = int(kwargs.get('gpu_device')) if 'gpu_device' in kwargs and kwargs['gpu_device'] else None

    text2text_generation_transformation = Text2TextGenerationTransformation(model, input_field, output_field,
                                                                            max_length=max_length,
                                                                            max_new_tokens=max_new_tokens,
                                                                            min_length=min_length,
                                                                            min_new_tokens=min_new_tokens,
                                                                            do_sample=do_sample,
                                                                            num_beams=num_beams,
                                                                            temperature=temperature,
                                                                            top_k=top_k,
                                                                            gpu_device=gpu_device)
    return text2text_generation_transformation.transform
