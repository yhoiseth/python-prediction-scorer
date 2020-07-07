import math
import statistics
from decimal import Decimal
from typing import List, Optional, Tuple, Union

from predictionscorer.choice.calculators import (
    brier_score,
    logarithmic_score,
    practical_score,
    quadratic_score,
)

ONE = Decimal(1)
TWO = Decimal(2)
ONE_HUNDRED = Decimal(100)


def log(value: Decimal) -> Decimal:
    return Decimal(str(math.log2(value)))


def to_decimal(probability: Union[Decimal, float, int]) -> Decimal:
    if isinstance(probability, Decimal):
        return probability
    if isinstance(probability, float):
        # Floats are sometimes converted imprecisely.
        return Decimal(str(probability))
    return Decimal(probability)


def median(scores: List[Decimal]) -> Decimal:
    return Decimal(statistics.median(scores))


class Collection:
    median_brier: Decimal
    median_logarithmic: Decimal
    median_practical: Decimal
    median_quadratic: Decimal
    predictions: Tuple["Prediction", ...]

    def __init__(self, predictions: Tuple["Prediction", ...]):
        (
            brier_scores,
            logarithmic_scores,
            practical_scores,
            quadratic_scores,
        ) = self.collect_scores(predictions)
        self.median_brier = median(brier_scores)
        self.median_logarithmic = median(logarithmic_scores)
        self.median_practical = median(practical_scores)
        self.median_quadratic = median(quadratic_scores)
        self.set_relative_scores(predictions)

    def set_relative_scores(self, predictions):
        for prediction in predictions:
            prediction.relative_brier = prediction.brier - self.median_brier
            prediction.relative_practical = prediction.practical - self.median_practical
            prediction.relative_logarithmic = (
                prediction.logarithmic - self.median_logarithmic
            )
            prediction.relative_quadratic = prediction.quadratic - self.median_quadratic
        self.predictions = predictions

    @staticmethod
    def collect_scores(
        predictions: Tuple["Prediction", ...]
    ) -> Tuple[
        List[Decimal], List[Decimal], List[Decimal], List[Decimal],
    ]:
        brier_scores: List[Decimal] = []
        logarithmic_scores: List[Decimal] = []
        practical_scores: List[Decimal] = []
        quadratic_scores: List[Decimal] = []
        for prediction in predictions:
            brier_scores.append(prediction.brier)
            logarithmic_scores.append(prediction.logarithmic)
            practical_scores.append(prediction.practical)
            quadratic_scores.append(prediction.quadratic)
        return brier_scores, logarithmic_scores, practical_scores, quadratic_scores


class Prediction:
    _brier: Optional[Decimal] = None
    _inverse_probability: Decimal
    _logarithmic: Optional[Decimal] = None
    _max_practical_score: Decimal
    _max_probability: Decimal
    _practical: Optional[Decimal] = None
    _quadratic: Optional[Decimal] = None
    probability: Decimal
    relative_brier: Optional[Decimal]
    relative_logarithmic: Optional[Decimal]
    relative_practical: Optional[Decimal]
    relative_quadratic: Optional[Decimal]

    def __init__(
        self,
        probability: Union[Decimal, float, int],
        max_practical_score: Union[Decimal, float, int] = TWO,
        max_probability: Union[Decimal, float, int] = Decimal("0.9999"),
    ):
        assert 0 <= probability <= 1
        assert max_probability <= 1
        self.probability = to_decimal(probability)
        self._inverse_probability = ONE - self.probability
        self._max_practical_score = to_decimal(max_practical_score)
        self._max_probability = to_decimal(max_probability)

    @property
    def brier(self) -> Decimal:
        if isinstance(self._brier, Decimal):
            return self._brier
        self._brier = brier_score(self.probability)
        return self._brier

    @property
    def quadratic(self) -> Decimal:
        if isinstance(self._quadratic, Decimal):
            return self._quadratic
        self._quadratic = quadratic_score(self.probability)
        return self._quadratic

    @property
    def logarithmic(self) -> Decimal:
        if isinstance(self._logarithmic, Decimal):
            return self._logarithmic
        self._logarithmic = logarithmic_score(self.probability)
        return self._logarithmic

    @property
    def practical(self) -> Decimal:
        if isinstance(self._practical, Decimal):
            return self._practical
        self._practical = practical_score(
            self.probability, self._max_probability, self._max_practical_score
        )
        return self._practical
