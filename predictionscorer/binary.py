from decimal import Decimal
from typing import Optional


class Prediction:
    _brier: Optional[Decimal] = None
    probability: Decimal

    def __init__(self, probability):
        self.probability = (
            probability if isinstance(probability, Decimal) else Decimal(probability)
        )

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
