from decimal import Decimal
from typing import Optional, Union


class Prediction:
    _brier: Optional[Decimal] = None
    probability: Decimal

    def __init__(self, probability: Union[Decimal, float, int]):
        self.probability = self.convert_probability(probability)

    def convert_probability(self, probability: Union[Decimal, float, int]) -> Decimal:
        if isinstance(probability, Decimal):
            return probability
        if isinstance(probability, int):
            return Decimal(probability)
        return Decimal(str(probability))  # Floats are sometimes converted imprecisely.

    @property
    def brier(self) -> Decimal:
        if isinstance(self._brier, Decimal):
            return self._brier
        one = Decimal(1)
        exponent = Decimal(2)
        probability_true = self.probability / Decimal(100)
        probability_false = one - probability_true
        self._brier = (
            probability_true - one
        ) ** exponent + probability_false ** exponent
        return self._brier
