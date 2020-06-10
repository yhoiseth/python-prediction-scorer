from predictionscorer.binary import Prediction


class TestBrier:
    def test_0_percent(self):
        probability = 0
        prediction = Prediction(probability)
        assert prediction.probability == 0
        assert prediction.brier == 2
