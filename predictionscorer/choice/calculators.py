from decimal import Decimal
from typing import Union

from predictionscorer.common import to_decimal

ONE = Decimal(1)
TWO = Decimal(2)


def inverse_probability(probability: Decimal) -> Decimal:
    return ONE - probability


def brier_score(probability: Union[Decimal, float, int]) -> Decimal:
    probability = to_decimal(probability)
    return TWO * (inverse_probability(probability) ** TWO)


def quadratic_score(probability: Union[Decimal, float, int]) -> Decimal:
    probability = to_decimal(probability)
    inverse = inverse_probability(probability)
    return probability * (TWO - probability) - inverse ** TWO
