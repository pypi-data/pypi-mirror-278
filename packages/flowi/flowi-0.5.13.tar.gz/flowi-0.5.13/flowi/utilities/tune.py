from typing import Union, Any

import numpy as np
from hyperopt import hp


def _cast_to_type(values: Union[list, str, int, float, bool, dict, None], value_type: type) -> Union[list, str, int, float, bool, dict, None]:
    if isinstance(values, dict) or values is None:
        return values

    elif isinstance(values, list):
        if isinstance(values[0], dict):
            return values
        try:
            return [value_type(item) for item in values]
        except ValueError:
            return None
    else:
        try:
            return value_type(values)
        except ValueError:
            return None


def tune_param(label: str,
               values: Union[list, str, int, float, bool, dict, None],
               value_type: type,
               method: str = "",
               min_value: Union[int, float] = -np.inf,
               max_value: Union[int, float] = np.inf
               ):
    print(f"tunning param: {label} | type: {type(values)}")
    values = _cast_to_type(values=values, value_type=value_type)

    if isinstance(values, list):
        print(f"tunning param element: {label} | type: {type(values[0])}")

    if method:
        if isinstance(values, list):
            return getattr(hp, method)(label, values)
        else:
            return getattr(hp, method)(label, [values])

    if isinstance(values, str) or isinstance(values, bool) or isinstance(values, dict) or values is None:
        return hp.choice(label, [values])
    elif isinstance(values, int):
        return hp.randint(label, max(min_value, int(values / 2)), min(max_value, int(values * 2)))
    elif isinstance(values, float):
        return hp.uniform(label, max(min_value, values / 2), min(max_value, values * 2))
    elif isinstance(values, list):
        if isinstance(values[0], str) or isinstance(values[0], bool) or isinstance(values, dict) or values[0] is None:
            return hp.choice(label, values)
        elif isinstance(values[0], int):
            if len(values) == 2:
                return hp.randint(label, max(min_value, values[0]), min(max_value, values[-1]))
            else:
                return hp.choice(label, values)
        else:
            if len(values) == 2:
                return hp.uniform(label, max(min_value, values[0]), min(max_value, values[-1]))
            else:
                return hp.choice(label, values)
    else:
        raise ValueError("Tune param error. Not sure which method to use."
                         f"Label: {label}, values: {values}")
