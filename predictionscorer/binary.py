import math
from decimal import Decimal
from typing import Optional, Union

ONE = Decimal(1)
TWO = Decimal(2)
ONE_HUNDRED = Decimal(100)


def log(value: Decimal) -> Decimal:
    return Decimal(str(math.log2(value)))


def convert_probability(probability: Union[Decimal, float, int]) -> Decimal:
    if isinstance(probability, float):
        # Floats are sometimes converted imprecisely.
        probability = Decimal(str(probability))
    elif not isinstance(probability, Decimal):
        probability = Decimal(probability)
    return probability / ONE_HUNDRED


class Prediction:
    _brier: Optional[Decimal] = None
    _inverse_probability: Decimal
    _logarithmic: Optional[Decimal] = None
    _max_practical_score: Decimal
    _max_probability: Decimal
    _practical: Optional[Decimal] = None
    _probability: Decimal
    _quadratic: Optional[Decimal] = None

    def __init__(
        self,
        probability_in_percent: Union[Decimal, float, int],
        max_practical_score=ONE_HUNDRED,
        max_probability=Decimal("99.99"),
    ):
        self._probability = convert_probability(probability_in_percent)
        self._inverse_probability = ONE - self._probability
        self._max_practical_score = max_practical_score
        self._max_probability = convert_probability(max_probability)

    @property
    def brier(self) -> Decimal:
        if isinstance(self._brier, Decimal):
            return self._brier
        self._brier = TWO * (self._inverse_probability ** TWO)
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

    @property
    def logarithmic(self) -> Decimal:
        if isinstance(self._logarithmic, Decimal):
            return self._logarithmic
        self._logarithmic = -Decimal(str(math.log2(self._probability)))
        return self._logarithmic

    @property
    def practical(self) -> Decimal:
        if isinstance(self._practical, Decimal):
            return self._practical
        nominator = self._max_practical_score * (log(self._probability) + ONE)
        denominator = log(self._max_probability + ONE)
        return nominator / denominator
