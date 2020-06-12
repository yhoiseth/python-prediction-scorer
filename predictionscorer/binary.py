from decimal import Decimal
from typing import Optional, Union


def convert_probability(probability: Union[Decimal, float, int]) -> Decimal:
    if isinstance(probability, float):
        # Floats are sometimes converted imprecisely.
        probability = Decimal(str(probability))
    elif not isinstance(probability, Decimal):
        probability = Decimal(probability)
    return probability / Decimal(100)


class Prediction:
    _brier: Optional[Decimal] = None
    _quadratic: Optional[Decimal] = None
    _inverse_probability: Decimal
    _probability: Decimal

    def __init__(self, probability_in_percent: Union[Decimal, float, int]):
        self._probability = convert_probability(probability_in_percent)
        self._inverse_probability = Decimal(1) - self._probability

    @property
    def brier(self) -> Decimal:
        if isinstance(self._brier, Decimal):
            return self._brier
        one = Decimal(1)
        exponent = Decimal(2)
        probability_false = one - self._probability
        self._brier = (
            one - self._probability
        ) ** exponent + probability_false ** exponent
        return self._brier

    @property
    def quadratic(self) -> Decimal:
        return self._probability * (
            Decimal(2) - self._probability
        ) + self._inverse_probability * (-self._inverse_probability)
