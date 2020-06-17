from decimal import Decimal

import pytest

from predictionscorer.binary import Collection, Prediction


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


class TestRelativeBrier:
    def test_40_65(self):
        collection = Collection((Prediction(40), Prediction(65)))
        assert collection.median_brier == Decimal("0.4825")
        predictions = collection.predictions
        _40 = predictions[0]
        _65 = predictions[1]
        assert _40.relative_brier == Decimal("0.2375")
        assert _65.relative_brier == Decimal("-0.2375")


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
        assert Prediction(20).logarithmic == pytest.approx(Decimal("2.321"), abs=1e-3)

    def test_50_percent(self):
        assert Prediction(50).logarithmic == 1

    def test_80_percent(self):
        assert Prediction(80).logarithmic == pytest.approx(Decimal("0.321"), abs=1e-3)

    def test_100_percent(self):
        assert Prediction(100).logarithmic == 0


class TestPractical:
    def test_0_percent(self):
        with pytest.raises(ValueError):
            assert Prediction(0).practical == 0

    def test_20_percent(self):
        assert Prediction(20).practical == pytest.approx(Decimal("-132.202"), abs=1e-3)

    def test_50_percent(self):
        assert Prediction(50).practical == 0

    def test_80_percent(self):
        assert Prediction(80).practical == pytest.approx(Decimal("67.812"), abs=1e-3)

    def test_100_percent(self):
        assert Prediction(100).practical == 100
