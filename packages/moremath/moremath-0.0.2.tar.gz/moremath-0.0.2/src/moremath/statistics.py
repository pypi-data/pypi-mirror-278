from typing import List, Union
from collections import Counter
import statistics

def mean(data: List[Union[int, float]]) -> Union[int, float]:
    if not data:
        raise ValueError("Cannot calculate mean of empty list")
    return sum(data) / len(data)

def median(data: List[Union[int, float]]) -> Union[int, float]:
    if not data:
        raise ValueError("Cannot calculate median of empty list")
    return statistics.median(data)

def mode(data: List[Union[int, float]]) -> Union[int, float]:
    if not data:
        raise ValueError("Cannot calculate mode of empty list")
    counts = Counter(data)
    mode_values = counts.most_common(1)
    return mode_values[0][0]
