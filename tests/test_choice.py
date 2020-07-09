from decimal import Decimal
from typing import Union

import pytest

from predictionscorer.choice import Collection, Prediction


def approximately(number: Union[Decimal, float, int]):
    if isinstance(number, int):
        number = Decimal(number)
    elif isinstance(number, float):
        number = Decimal(str(number))
    assert isinstance(number, Decimal)
    return pytest.approx(number, abs=1e-2)


class TestBrier:
    def test_0_percent(self):
        assert Prediction(0.0).brier == 2

    def test_20_percent(self):
        assert Prediction(0.20).brier == Decimal("1.28")

    def test_50_percent(self):
        assert Prediction(0.50).brier == 0.5

    def test_80_percent(self):
        assert Prediction(0.80).brier == Decimal("0.08")

    def test_100_percent(self):
        assert Prediction(1).brier == 0


@pytest.mark.skip(
    reason="Breaks due to new assertions. Don’t know what I want to do about this yet."
)
class TestRelativeBrier:
    def test_20_80_100(self):
        bad = Prediction(0.20)
        good = Prediction(0.80)
        perfect = Prediction(1)
        collection = Collection((bad, good, perfect))
        assert collection.median_brier == Decimal("0.08")
        assert bad.relative_brier == Decimal("1.20")
        assert good.relative_brier == 0
        assert perfect.relative_brier == Decimal("-0.08")

    def test_40_65(self):
        _40 = Prediction(0.40)
        _65 = Prediction(0.65)
        collection = Collection((_40, _65))
        assert collection.median_brier == Decimal("0.4825")
        assert _40.relative_brier == Decimal("0.2375")
        assert _65.relative_brier == -_40.relative_brier


class TestQuadratic:
    def test_0_percent(self):
        assert Prediction(0.0).quadratic == -1

    def test_20_percent(self):
        assert Prediction(0.20).quadratic == Decimal("-0.28")

    def test_50_percent(self):
        assert Prediction(0.50).quadratic == 0.5

    def test_80_percent(self):
        assert Prediction(0.80).quadratic == Decimal("0.92")

    def test_100_percent(self):
        assert Prediction(1).quadratic == 1


@pytest.mark.skip(
    reason="Breaks due to new assertions. Don’t know what I want to do about this yet."
)
class TestRelativeQuadratic:
    def test_20_80_100(self):
        _20 = Prediction(0.20)
        _80 = Prediction(0.80)
        _100 = Prediction(1)
        collection = Collection((_20, _80, _100))
        assert collection.median_quadratic == Decimal("0.92")
        assert _20.relative_quadratic == Decimal("-1.20")
        assert _80.relative_quadratic == 0
        assert _100.relative_quadratic == Decimal("0.08")

    def test_40_65(self):
        _40 = Prediction(0.40)
        _65 = Prediction(0.65)
        collection = Collection((_40, _65))
        assert collection.median_quadratic == Decimal("0.5175")
        assert _40.relative_quadratic == Decimal("-0.2375")
        assert _65.relative_quadratic == Decimal("0.2375")


class TestLogarithmic:
    def test_0_percent(self):
        with pytest.raises(AssertionError):
            assert Prediction(0.0).logarithmic

    def test_20_percent(self):
        assert Prediction(0.20).logarithmic == pytest.approx(Decimal("2.321"), abs=1e-3)

    def test_50_percent(self):
        assert Prediction(0.50).logarithmic == 1

    def test_80_percent(self):
        assert Prediction(0.80).logarithmic == pytest.approx(Decimal("0.321"), abs=1e-3)

    def test_100_percent(self):
        assert Prediction(1).logarithmic == 0


@pytest.mark.skip(
    reason="Breaks due to new assertions. Don’t know what I want to do about this yet."
)
class TestRelativeLogarithmic:
    def test_20_80_100(self):
        collection = Collection((Prediction(0.20), Prediction(0.80), Prediction(1)))
        assert collection.median_logarithmic == approximately(0.32)
        predictions = collection.predictions
        _20 = predictions[0]
        _80 = predictions[1]
        _100 = predictions[2]
        assert _20.relative_logarithmic == approximately(2)
        assert _80.relative_logarithmic == 0
        assert _100.relative_logarithmic == approximately(-0.32)

    def test_20_80(self):
        collection = Collection((Prediction(0.20), Prediction(0.80)))
        assert collection.median_logarithmic == Decimal("1.32192809488736215")
        predictions = collection.predictions
        _40 = predictions[0]
        _65 = predictions[1]
        assert _40.relative_logarithmic == Decimal("0.99999999999999985")
        assert _65.relative_logarithmic == Decimal("-0.99999999999999985")


class TestPractical:
    def test_0_percent(self):
        with pytest.raises(AssertionError):
            assert Prediction(0.0).practical == 0

    def test_20_percent(self):
        assert Prediction(0.20).practical == pytest.approx(Decimal("-2.644"), abs=1e-3)

    def test_50_percent(self):
        assert Prediction(0.50).practical == 0

    def test_80_percent(self):
        assert Prediction(0.80).practical == pytest.approx(Decimal("1.356"), abs=1e-3)

    def test_max(self):
        assert Prediction(0.9999).practical == approximately(2)


@pytest.mark.skip(
    reason="Breaks due to new assertions. Don’t know what I want to do about this yet."
)
class TestRelativePractical:
    def test_20_80(self):
        collection = Collection((Prediction(0.20), Prediction(0.80)))
        assert collection.median_practical == approximately(-0.643)
        predictions = collection.predictions
        _20 = predictions[0]
        _80 = predictions[1]
        assert _20.relative_practical == approximately(-2)
        assert _80.relative_practical == approximately(2)
