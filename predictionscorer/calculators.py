import decimal

from predictionscorer import predictions


class Brier:
    true_alternative_index: int

    def __init__(self, true_alternative_index: int) -> None:
        self.true_alternative_index = true_alternative_index

    def calculate(self, prediction: predictions.Prediction) -> decimal.Decimal:
        score = decimal.Decimal(0.00)
        for index, probability in enumerate(prediction.probabilities):
            first_term = decimal.Decimal(probability) / decimal.Decimal(100)
            second_term = decimal.Decimal(
                1.00 if index == self.true_alternative_index else 0.00
            )
            score = score + (first_term - second_term) ** 2
        return score
