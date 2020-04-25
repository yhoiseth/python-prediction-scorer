from decimal import Decimal

from predictionscorer import calculators, predictions


class TestBrier:
    def test_readme_example(self):
        george = predictions.Prediction(probabilities=(Decimal(60), Decimal(40),))
        kramer = predictions.Prediction(probabilities=(Decimal(35), Decimal(65),))
        calculator = calculators.Brier(true_alternative_index=1,)
        assert calculator.calculate(george) == Decimal("0.72")
        assert calculator.calculate(kramer) == Decimal("0.245")

    def test_readme_example_more_than_two_alternatives(self):
        prediction = predictions.Prediction(
            probabilities=(Decimal(55), Decimal(35), Decimal(10),)
        )
        brier = calculators.Brier(true_alternative_index=1,)
        assert brier.calculate(prediction) == Decimal("0.735")

    def test_order_matters(self):
        prediction = predictions.Prediction(
            probabilities=(Decimal(25), Decimal(25), Decimal(30), Decimal(20),),
        )
        ordered_categorical = calculators.OrderedCategorical(true_alternative_index=1)
        assert ordered_categorical.calculate(prediction) == Decimal("0.2350")
