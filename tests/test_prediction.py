import decimal

import pytest

from predictionscorer import predictions


class TestPrediction:
    def test_probabilities_count(self):
        with pytest.raises(AssertionError) as assertion_error:
            predictions.Prediction(
                probabilities=[decimal.Decimal("100"),]
            )
        assert "A prediction needs at least two probabilities." in str(
            assertion_error.value
        )
