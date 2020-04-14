import typing


class Prediction:
    probabilities: typing.List[int]

    def __init__(self, probabilities: typing.List[int]) -> None:
        self.probabilities = probabilities
