from decimal import Decimal
from typing import Optional, Union


def convert_probability(probability: Union[Decimal, float, int]) -> Decimal:
    if isinstance(probability, Decimal):
        return probability
    if isinstance(probability, int):
        return Decimal(probability)
    return Decimal(str(probability))  # Floats are sometimes converted imprecisely.


class Prediction:
    _brier: Optional[Decimal] = None
    _quadratic: Optional[Decimal] = None
    probability: Decimal

    def __init__(self, probability: Union[Decimal, float, int]):
        self.probability = convert_probability(probability)

    @property
    def brier(self) -> Decimal:
        if isinstance(self._brier, Decimal):
            return self._brier
        one = Decimal(1)
        exponent = Decimal(2)
        probability_true = self.probability / Decimal(100)
        probability_false = one - probability_true
        self._brier = (
            one - probability_true
        ) ** exponent + probability_false ** exponent
        return self._brier
