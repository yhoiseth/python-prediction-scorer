import decimal
import typing

from predictionscorer import predictions


class Base:
    true_alternative_index: int

    def __init__(self, true_alternative_index: int) -> None:
        self.true_alternative_index = true_alternative_index


class Brier(Base):
    """
    Calculates scores when the order of predictions does not matter.
    """

    def calculate(self, prediction: predictions.Prediction) -> decimal.Decimal:
        score = decimal.Decimal("0.00")
        for index, probability in enumerate(prediction.probabilities):
            first_term = probability / decimal.Decimal(100)
            second_term = decimal.Decimal(
                "1.00" if index == self.true_alternative_index else "0.00"
            )
            score = score + (first_term - second_term) ** 2
        return score


class OrderedCategorical(Base):
    """
    Calculates scores when the order of predictions matters.
    """

    def calculate(self, prediction: predictions.Prediction) -> decimal.Decimal:
        total = decimal.Decimal("0.00")
        pair_count = self._pair_count(prediction.probabilities)
        for index in range(pair_count):
            pair = predictions.Prediction(
                self._split_probabilities(index, prediction.probabilities)
            )
            score = self._score_pair(index, pair)
            total += score
        return self._average(total, pair_count)

    @staticmethod
    def _pair_count(probabilities: typing.List[decimal.Decimal]) -> int:
        """
        We need one fewer pairs than the number of alternatives. For example, if there are three alternatives — A, B and C, the pairs are:

        - A and BC
        - AB and C
        """
        return len(probabilities) - 1

    @staticmethod
    def _average(total: decimal.Decimal, count: int) -> decimal.Decimal:
        return total / decimal.Decimal(count)

    def _score_pair(self, index: int, pair: predictions.Prediction) -> decimal.Decimal:
        assert len(pair.probabilities) == 2, "There must be exactly two probabilities."
        true_alternative_index = 0 if index > self.true_alternative_index else 1
        brier_calculator = Brier(true_alternative_index=true_alternative_index)
        return brier_calculator.calculate(pair)

    @staticmethod
    def _split_probabilities(
        index: int, probabilities: typing.List[decimal.Decimal]
    ) -> typing.List[decimal.Decimal]:
        """
        Given an index and a list of more than two probabilities, return a pair of grouped probabilities.
        """
        first_part = probabilities[: (index + 1)]
        second_part = probabilities[(index + 1) :]
        sum_first_part = decimal.Decimal(sum(first_part))
        sum_second_part = decimal.Decimal(sum(second_part))
        return [sum_first_part, sum_second_part]
