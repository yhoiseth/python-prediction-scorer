import typing
from decimal import Decimal


class Prediction:
    """
    This class encapsulates probabilities for a given question.
    """

    probabilities: typing.Tuple[Decimal, ...]
    true_alternative_index: int

    def __init__(
        self, probabilities: typing.Tuple[Decimal, ...], true_alternative_index: int
    ) -> None:
        """
        2 or more probabilities are required. Make sure that they sum to 100.
        """
        assert sum(probabilities) == 100, "Probabilities need to sum to 100."
        length = len(probabilities)
        assert length >= 2, "A prediction needs at least two probabilities."
        assert (
            true_alternative_index >= 0
        ), "The true alternative index cannot be negative"
        assert (
            true_alternative_index <= length - 1
        ), "Probabilities need to contain the true alternative"
        self.probabilities = probabilities
