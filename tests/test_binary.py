from decimal import Decimal

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

    def test_100_percent(self):
        assert Prediction(100).quadratic == 1
