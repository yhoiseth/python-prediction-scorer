import math
from decimal import Decimal
from typing import Union


def to_decimal(probability: Union[Decimal, float, int]) -> Decimal:
    if isinstance(probability, Decimal):
        return probability
    if isinstance(probability, float):
        # Floats are sometimes converted imprecisely.
        return Decimal(str(probability))
    return Decimal(probability)


def inverse_probability(probability: Decimal) -> Decimal:
    return Decimal(1) - probability


def log(value: Decimal) -> Decimal:
    return Decimal(str(math.log2(value)))
