import math
from decimal import Decimal

import pytest

from predictionscorer.binary import Prediction


class TestBrier:
    def test_0_percent(self):
        assert Prediction(0).brier == 2

    def test_20_percent(self):
        assert Prediction(20).brier == Decimal("1.28")

    def test_50_percent(self):
        assert Prediction(50).brier == 0.5

    def test_80_percent(self):
        assert Prediction(80).brier == Decimal("0.08")

    def test_100_percent(self):
        assert Prediction(100).brier == 0


class TestQuadratic:
    def test_0_percent(self):
        assert Prediction(0).quadratic == -1

    def test_20_percent(self):
        assert Prediction(20).quadratic == Decimal("-0.28")

    def test_50_percent(self):
        assert Prediction(50).quadratic == 0.5

    def test_80_percent(self):
        assert Prediction(80).quadratic == Decimal("0.92")

    def test_100_percent(self):
        assert Prediction(100).quadratic == 1


class TestLogarithmic:
    def test_0_percent(self):
        with pytest.raises(ValueError):
            assert Prediction(0).logarithmic

    def test_20_percent(self):
        assert Prediction(20).logarithmic == pytest.approx(Decimal("0.699"), abs=1e-3)

    def test_50_percent(self):
        assert Prediction(50).logarithmic == pytest.approx(Decimal("0.301"), abs=1e-3)

    def test_80_percent(self):
        assert Prediction(80).logarithmic == pytest.approx(Decimal("0.097"), abs=1e-3)

    def test_100_percent(self):
        assert Prediction(100).logarithmic == 0
