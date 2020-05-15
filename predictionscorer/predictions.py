import typing
from decimal import Decimal


class Prediction:
    """
    This class encapsulates probabilities for a given question.
    """

    _cached_brier_score: typing.Optional[Decimal] = None
    probabilities: typing.Tuple[Decimal, ...]
    true_alternative_index: int

    def __init__(
        self,
        probabilities: typing.Tuple[Decimal, ...],
        true_alternative_index: int,
        order_matters: bool = False,
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
        self.true_alternative_index = true_alternative_index

    @property
    def brier_score(self) -> Decimal:
        if isinstance(self._cached_brier_score, Decimal):
            return self._cached_brier_score
        score = Decimal("0.00")
        for index, probability in enumerate(self.probabilities):
            first_term = probability / Decimal(100)
            second_term = Decimal(
                "1.00" if index == self.true_alternative_index else "0.00"
            )
            score = score + (first_term - second_term) ** Decimal(2)
        self._cached_brier_score = score
        return score
