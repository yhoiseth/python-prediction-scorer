import decimal

from predictionscorer import calculators, predictions


class TestBrier:
    def test_readme_example(self):
        george = predictions.Prediction(
            probabilities=[decimal.Decimal(60), decimal.Decimal(40),]
        )
        kramer = predictions.Prediction(
            probabilities=[decimal.Decimal(35), decimal.Decimal(65),]
        )
        calculator = calculators.Brier(true_alternative_index=1,)
        assert calculator.calculate(george) == decimal.Decimal("0.72")
        assert calculator.calculate(kramer) == decimal.Decimal("0.245")

    def test_readme_example_more_than_two_alternatives(self):
        prediction = predictions.Prediction(
            probabilities=[
                decimal.Decimal(55),
                decimal.Decimal(35),
                decimal.Decimal(10),
            ]
        )
        brier = calculators.Brier(true_alternative_index=1,)
        assert brier.calculate(prediction) == decimal.Decimal("0.735")

    def test_order_matters(self):
        prediction = predictions.Prediction(
            probabilities=[
                decimal.Decimal(25),
                decimal.Decimal(25),
                decimal.Decimal(50),
                decimal.Decimal(0),
            ],
        )

        brier = calculators.Brier(true_alternative_index=1, order_matters=True,)

        assert brier.calculate(prediction) == decimal.Decimal("0.208")
