from decimal import Decimal

import pytest

from predictionscorer import predictions


class TestInitialization:
    def test_probabilities_count(self):
        with pytest.raises(AssertionError) as assertion_error:
            predictions.Prediction(
                probabilities=(Decimal("100"),), true_alternative_index=0
            )
        assert "A prediction needs at least two probabilities." in str(
            assertion_error.value
        )

    def test_probabilities_sum_more_than_100(self):
        with pytest.raises(AssertionError) as assertion_error:
            predictions.Prediction(
                probabilities=(Decimal("75"), Decimal("25.01"),),
                true_alternative_index=0,
            )
        assert "Probabilities need to sum to 100." in str(assertion_error.value)

    def test_probabilities_sum_less_than_100(self):
        with pytest.raises(AssertionError) as assertion_error:
            predictions.Prediction(
                probabilities=(Decimal("75"), Decimal("24.99"),),
                true_alternative_index=1,
            )
        assert "Probabilities need to sum to 100." in str(assertion_error.value)

    def test_true_alternative_index_not_in_probabilities(self):
        with pytest.raises(AssertionError) as assertion_error:
            predictions.Prediction(
                probabilities=(Decimal("75"), Decimal("25"),), true_alternative_index=2
            )
        assert "Probabilities need to contain the true alternative" in str(
            assertion_error.value
        )

    def test_negative_true_alternative_index(self):
        with pytest.raises(AssertionError) as assertion_error:
            predictions.Prediction(
                probabilities=(Decimal("75"), Decimal("25"),), true_alternative_index=-1
            )
        assert "The true alternative index cannot be negative" in str(
            assertion_error.value
        )


class TestBrier:
    def test_60_40_with_cache(self):
        prediction = predictions.Prediction(
            probabilities=(Decimal(60), Decimal(40),), true_alternative_index=1,
        )
        assert prediction._cached_brier_score is None
        score = prediction.brier_score
        assert score == prediction._cached_brier_score
        assert score == Decimal("0.72")

    def test_35_65(self):
        prediction = predictions.Prediction(
            probabilities=(Decimal(35), Decimal(65),), true_alternative_index=1,
        )
        assert prediction.brier_score == Decimal("0.245")

    def test_readme_example_more_than_two_alternatives(self):
        prediction = predictions.Prediction(
            probabilities=(Decimal(55), Decimal(35), Decimal(10),),
            true_alternative_index=1,
        )
        assert prediction.brier_score == Decimal("0.735")

    def test_order_matters(self):
        prediction = predictions.Prediction(
            probabilities=(Decimal(25), Decimal(25), Decimal(30), Decimal(20),),
            true_alternative_index=1,
            order_matters=True,
        )

        assert prediction.brier_score == Decimal("0.2350")
