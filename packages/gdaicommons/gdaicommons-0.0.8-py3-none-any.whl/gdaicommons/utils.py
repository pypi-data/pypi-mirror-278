from typing import Dict, List, Optional, Union


def normalize_model_output(output: Union[List[List[Dict]], List[Dict]]) -> List[List[Dict]]:
    if not output:
        return []

    if isinstance(output[0], list):
        return output
    else:
        return [output]


def parse_parameter(param: Optional[str], cast_class):
    if not param:
        return param

    return cast_class(param)


def blank_if_null(param: str) -> str:
    if param is None:
        return ""
    return param
