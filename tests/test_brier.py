import decimal

from predictionscorer import predictions
from predictionscorer import (
    calculators,
)  # Brier scoring is arguably the most common way of scoring predictions.


class TestBrier:
    def test_readme(self):
        george = predictions.Prediction(
            probabilities=[60, 40]
        )  # George put Clinton at 60 % and Trump at 40 %.
        kramer = predictions.Prediction(
            probabilities=[35, 65]
        )  # Kramer put Clinton at 35 % and Trump at 65 %.

        calculator = calculators.Brier(
            true_alternative_index=1
        )  # Alternative 0 is Hillary Clinton. Alternative 1 is Donald Trump.

        assert calculator.calculate(george) == decimal.Decimal("0.72")
        assert calculator.calculate(kramer) == decimal.Decimal("0.245")
