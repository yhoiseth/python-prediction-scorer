import decimal
import typing


class Prediction:
    probabilities: typing.List[decimal.Decimal]

    def __init__(self, probabilities: typing.List[decimal.Decimal]) -> None:
        self.probabilities = probabilities
