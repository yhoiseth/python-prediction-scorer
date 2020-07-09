import pytest

from predictionscorer.choice import (
    brier_score,
    logarithmic_score,
    practical_score,
    quadratic_score,
)


class TestBrier:
    def test_0_percent(self):
        assert brier_score(0.0) == 2

    def test_20_percent(self):
        assert brier_score(0.20) == 1.28

    def test_50_percent(self):
        assert brier_score(0.50) == 0.5

    def test_80_percent(self):
        assert brier_score(0.80) == 0.08

    def test_100_percent(self):
        assert brier_score(1) == 0


class TestQuadratic:
    def test_0_percent(self):
        assert quadratic_score(0.0) == -1

    def test_20_percent(self):
        assert quadratic_score(0.20) == -0.28

    def test_50_percent(self):
        assert quadratic_score(0.50) == 0.5

    def test_80_percent(self):
        assert quadratic_score(0.80) == 0.92

    def test_100_percent(self):
        assert quadratic_score(1) == 1


class TestLogarithmic:
    def test_0_percent(self):
        with pytest.raises(AssertionError):
            assert logarithmic_score(0.0)

    def test_20_percent(self):
        assert logarithmic_score(0.20) == 2.32

    def test_50_percent(self):
        assert logarithmic_score(0.50) == 1

    def test_80_percent(self):
        assert logarithmic_score(0.80) == 0.32

    def test_100_percent(self):
        assert logarithmic_score(1) == 0


class TestPractical:
    def test_0_percent(self):
        with pytest.raises(AssertionError):
            assert practical_score(0.0) == 0

    def test_20_percent(self):
        assert practical_score(0.20) == -2.64

    def test_50_percent(self):
        assert practical_score(0.50) == 0

    def test_80_percent(self):
        assert practical_score(0.80) == 1.36

    def test_max(self):
        assert practical_score(0.9999) == 2
