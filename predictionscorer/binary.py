import math
import statistics
from decimal import Decimal
from typing import List, Optional, Tuple, Union

ONE = Decimal(1)
TWO = Decimal(2)
ONE_HUNDRED = Decimal(100)


def log(value: Decimal) -> Decimal:
    return Decimal(str(math.log2(value)))


def convert_probability(probability: Union[Decimal, float, int]) -> Decimal:
    if isinstance(probability, float):
        # Floats are sometimes converted imprecisely.
        probability = Decimal(str(probability))
    elif not isinstance(probability, Decimal):
        probability = Decimal(probability)
    return probability / ONE_HUNDRED


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
    _probability: Decimal
    _quadratic: Optional[Decimal] = None
    relative_brier: Optional[Decimal]
    relative_logarithmic: Optional[Decimal]
    relative_practical: Optional[Decimal]
    relative_quadratic: Optional[Decimal]

    def __init__(
        self,
        probability_in_percent: Union[Decimal, float, int],
        max_practical_score=ONE_HUNDRED,
        max_probability=Decimal("99.99"),
    ):
        self._probability = convert_probability(probability_in_percent)
        self._inverse_probability = ONE - self._probability
        self._max_practical_score = max_practical_score
        self._max_probability = convert_probability(max_probability)

    @property
    def brier(self) -> Decimal:
        if isinstance(self._brier, Decimal):
            return self._brier
        self._brier = TWO * (self._inverse_probability ** TWO)
        return self._brier

    @property
    def quadratic(self) -> Decimal:
        if isinstance(self._quadratic, Decimal):
            return self._quadratic
        self._quadratic = (
            self._probability * (TWO - self._probability)
            - self._inverse_probability ** TWO
        )
        return self._quadratic

    @property
    def logarithmic(self) -> Decimal:
        if isinstance(self._logarithmic, Decimal):
            return self._logarithmic
        self._logarithmic = -log(self._probability)
        return self._logarithmic

    @property
    def practical(self) -> Decimal:
        if isinstance(self._practical, Decimal):
            return self._practical
        nominator = self._max_practical_score * (log(self._probability) + ONE)
        denominator = log(self._max_probability + ONE)
        score = nominator / denominator
        if score > self._max_practical_score:
            score = self._max_practical_score
        self._practical = score
        return self._practical
