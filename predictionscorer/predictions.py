import decimal
import typing


class Prediction:
    probabilities: typing.List[decimal.Decimal]

    def __init__(self, probabilities: typing.List[decimal.Decimal]) -> None:
        assert len(probabilities) >= 2, "A prediction needs at least two probabilities."
        assert sum(probabilities) == 100, "Probabilities need to sum to 100."
        self.probabilities = probabilities
