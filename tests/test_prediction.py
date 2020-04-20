import decimal

import pytest

from predictionscorer import predictions


class TestPrediction:
    def test_probabilities_count(self):
        with pytest.raises(AssertionError) as assertion_error:
            predictions.Prediction(probabilities=(decimal.Decimal("100"),),)
        assert "A prediction needs at least two probabilities." in str(
            assertion_error.value
        )

    def test_probabilities_sum_more_than_100(self):
        with pytest.raises(AssertionError) as assertion_error:
            predictions.Prediction(
                probabilities=(decimal.Decimal("75"), decimal.Decimal("25.01"),),
            )
        assert "Probabilities need to sum to 100." in str(assertion_error.value)

    def test_probabilities_sum_less_than_100(self):
        with pytest.raises(AssertionError) as assertion_error:
            predictions.Prediction(
                probabilities=(decimal.Decimal("75"), decimal.Decimal("24.99"),),
            )
        assert "Probabilities need to sum to 100." in str(assertion_error.value)
