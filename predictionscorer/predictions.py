import decimal
import typing


class Prediction:
    """
    This class encapsulates probabilities for a given question.
    """

    probabilities: typing.List[decimal.Decimal]

    def __init__(self, probabilities: typing.List[decimal.Decimal]) -> None:
        """
        2 or more probabilities are required. Make sure that they sum to 100.
        """
        assert len(probabilities) >= 2, "A prediction needs at least two probabilities."
        assert sum(probabilities) == 100, "Probabilities need to sum to 100."
        self.probabilities = probabilities
