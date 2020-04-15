import decimal

from predictionscorer import calculators, predictions


class TestBrier:
    def test_readme_example(self):
        george = predictions.Prediction(probabilities=[60, 40])
        kramer = predictions.Prediction(probabilities=[35, 65])
        calculator = calculators.Brier(true_alternative_index=1)
        assert calculator.calculate(george) == decimal.Decimal("0.72")
        assert calculator.calculate(kramer) == decimal.Decimal("0.245")

    def test_readme_example_more_than_two_alternatives(self):
        prediction = predictions.Prediction(probabilities=[55, 35, 10,])
        brier = calculators.Brier(true_alternative_index=1,)
        assert brier.calculate(prediction) == decimal.Decimal("0.735")
