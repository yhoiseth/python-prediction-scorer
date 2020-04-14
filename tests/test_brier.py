import decimal

from predictionscorer import calculators, predictions


class TestBrier:
    def test_readme_example(self):
        george = predictions.Prediction(probabilities=[60, 40])
        kramer = predictions.Prediction(probabilities=[35, 65])
        calculator = calculators.Brier(true_alternative_index=1)
        assert calculator.calculate(george) == decimal.Decimal("0.72")
        assert calculator.calculate(kramer) == decimal.Decimal("0.245")
