from decimal import Decimal
from typing import Optional, Union


def to_decimal(probability: Union[Decimal, float, int]) -> Decimal:
    if isinstance(probability, Decimal):
        return probability
    if isinstance(probability, float):
        # Floats are sometimes converted imprecisely.
        return Decimal(str(probability))
    return Decimal(probability)


class Score:
    decimal_places: int
    _rounded: Optional[Decimal]
    value: Decimal

    def __init__(self, value: Decimal, decimal_places: int = 2):
        self.value = value
        self.decimal_places = decimal_places

    @property
    def rounded(self) -> Decimal:
        if isinstance(self._rounded, Decimal):
            return self._rounded
        self._rounded = Decimal(round(self.value, self.decimal_places))
        return self._rounded

    def __str__(self) -> str:
        return str(self.rounded)
