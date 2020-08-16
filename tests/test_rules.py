from decimal import Decimal
from typing import Union

import pytest

from predictionscorer.rules import (
    brier_score,
    distance_score,
    logarithmic_score,
    practical_score,
    quadratic_score,
)


def approximately(number: Union[Decimal, float, int]):
    if isinstance(number, int):
        number = Decimal(number)
    elif isinstance(number, float):
        number = Decimal(str(number))
    assert isinstance(number, Decimal)
    return pytest.approx(number, abs=1e-2)


class TestBrier:
    def test_0_percent(self):
        assert brier_score(0.0) == 2

    def test_20_percent(self):
        assert brier_score(0.20) == Decimal("1.28")

    def test_50_percent(self):
        assert brier_score(0.50) == 0.5

    def test_80_percent(self):
        assert brier_score(0.80) == Decimal("0.08")

    def test_100_percent(self):
        assert brier_score(1) == 0


class TestDistance:
    def test_example(self):
        score = distance_score(10, 5, 15)
        assert score == approximately(9.091)

    def test_perfect_95_percent(self):
        with pytest.raises(ValueError):
            distance_score(10, 10, 10)


class TestLogarithmic:
    def test_0_percent(self):
        with pytest.raises(AssertionError):
            assert logarithmic_score(0.0)

    def test_20_percent(self):
        assert logarithmic_score(0.20) == approximately(2.321)

    def test_50_percent(self):
        assert logarithmic_score(0.50) == 1

    def test_80_percent(self):
        assert logarithmic_score(0.80) == approximately(0.321)

    def test_100_percent(self):
        assert logarithmic_score(1) == 0


class TestPractical:
    def test_0_percent(self):
        with pytest.raises(AssertionError):
            assert practical_score(0.0) == 0

    def test_20_percent(self):
        assert practical_score(0.20) == approximately(-2.644)

    def test_50_percent(self):
        assert practical_score(0.50) == 0

    def test_80_percent(self):
        assert practical_score(0.80) == approximately(1.356)

    def test_max(self):
        assert practical_score(0.9999) == approximately(2)


class TestQuadratic:
    def test_0_percent(self):
        assert quadratic_score(0.0) == -1

    def test_20_percent(self):
        assert quadratic_score(0.20) == Decimal("-0.28")

    def test_50_percent(self):
        assert quadratic_score(0.50) == 0.5

    def test_80_percent(self):
        assert quadratic_score(0.80) == Decimal("0.92")

    def test_100_percent(self):
        assert quadratic_score(1) == 1
