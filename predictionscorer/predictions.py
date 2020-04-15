import decimal
import typing


class Prediction:
    probabilities: typing.List[decimal.Decimal]

    def __init__(self, probabilities: typing.List[decimal.Decimal]) -> None:
        assert len(probabilities) >= 2, "A prediction needs at least two probabilities."
        self.probabilities = probabilities
