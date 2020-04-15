import decimal
import typing

from predictionscorer import predictions


class Base:
    true_alternative_index: int

    def __init__(self, true_alternative_index: int) -> None:
        self.true_alternative_index = true_alternative_index


class Brier(Base):
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
    def calculate(self, prediction: predictions.Prediction) -> decimal.Decimal:
        total = decimal.Decimal("0.00")
        for index, probability in enumerate(prediction.probabilities):
            if index == len(prediction.probabilities) - 1:
                break
            first_part = prediction.probabilities[: (index + 1)]
            second_part = prediction.probabilities[(index + 1) :]
            sum_first_part = decimal.Decimal(sum(first_part))
            sum_second_part = decimal.Decimal(sum(second_part))
            pair = predictions.Prediction([sum_first_part, sum_second_part])
            true_alternative_index = 0 if index > self.true_alternative_index else 1
            brier_calculator = Brier(true_alternative_index=true_alternative_index)
            brier_score = brier_calculator.calculate(pair)
            total += brier_score
        average = total / decimal.Decimal(len(prediction.probabilities) - 1)
        return average
