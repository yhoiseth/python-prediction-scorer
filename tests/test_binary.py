from predictionscorer.binary import Prediction


class TestBrier:
    def test_0_percent(self):
        assert Prediction(0).brier == 2

    def test_50_percent(self):
        assert Prediction(50).brier == 0.5

    def test_100_percent(self):
        assert Prediction(100).brier == 0
