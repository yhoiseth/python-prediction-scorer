from decimal import Decimal
from typing import Optional, Union

ONE = Decimal(1)
TWO = Decimal(2)


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
        self._inverse_probability = ONE - self._probability

    @property
    def brier(self) -> Decimal:
        if isinstance(self._brier, Decimal):
            return self._brier
        self._brier = 2 * (self._inverse_probability ** TWO)
        return self._brier

    @property
    def quadratic(self) -> Decimal:
        if isinstance(self._quadratic, Decimal):
            return self._quadratic
        self._quadratic = (
            self._probability * (TWO - self._probability)
            - self._inverse_probability ** TWO
        )
        return self._quadratic
