import datetime
import statistics
import typing
from dataclasses import dataclass
from decimal import Decimal


class Base:
    true_alternative_index: int

    def __init__(self, true_alternative_index: int) -> None:
        self.true_alternative_index = true_alternative_index


class Brier(Base):
    """
    Calculates scores when the order of predictions does not matter.
    """

    def calculate(self, prediction: "Prediction") -> Decimal:
        score = Decimal("0.00")
        for index, probability in enumerate(prediction.probabilities):
            first_term = probability / Decimal(100)
            second_term = Decimal(
                "1.00" if index == self.true_alternative_index else "0.00"
            )
            score = score + (first_term - second_term) ** 2
        return score


class OrderedCategorical(Base):
    """
    Calculates scores when the order of predictions matters.
    """

    def calculate(self, prediction: "Prediction") -> Decimal:
        total = Decimal("0.00")
        pair_count = self._pair_count(prediction.probabilities)
        for index in range(pair_count):
            pair = Prediction(
                self._split_probabilities(index, prediction.probabilities),
                true_alternative_index=1,
            )
            score = self._score_pair(index, pair)
            total += score
        return self._average(total, pair_count)

    @staticmethod
    def _pair_count(probabilities: typing.Tuple[Decimal, ...]) -> int:
        """
        We need one fewer pairs than the number of alternatives. For example, if there are three alternatives — A, B and C, the pairs are:

        - A and BC
        - AB and C
        """
        return len(probabilities) - 1

    @staticmethod
    def _average(total: Decimal, count: int) -> Decimal:
        return total / Decimal(count)

    def _score_pair(self, index: int, pair: "Prediction") -> Decimal:
        assert len(pair.probabilities) == 2, "There must be exactly two probabilities."
        true_alternative_index = 0 if index > self.true_alternative_index else 1
        brier_calculator = Brier(true_alternative_index=true_alternative_index)
        return brier_calculator.calculate(pair)

    @staticmethod
    def _split_probabilities(
        index: int, probabilities: typing.Tuple[Decimal, ...]
    ) -> typing.Tuple[Decimal, Decimal]:
        """
        Given an index and a tuple of more than two probabilities, return a pair of grouped probabilities.
        """
        assert len(probabilities) > 2
        first_part = probabilities[: (index + 1)]
        second_part = probabilities[(index + 1) :]
        sum_first_part = Decimal(sum(first_part))
        sum_second_part = Decimal(sum(second_part))
        return sum_first_part, sum_second_part


class Prediction:
    """
    This class encapsulates probabilities for a given question.
    """

    _cached_brier_score: typing.Optional[Decimal] = None
    created_at: typing.Optional[datetime.datetime]
    created_by: typing.Optional[str]
    created_on: typing.Optional[datetime.date]
    order_matters: bool
    probabilities: typing.Tuple[Decimal, ...]
    relative_brier_score: typing.Optional[Decimal] = None
    true_alternative_index: int

    def __init__(
        self,
        probabilities: typing.Tuple[Decimal, ...],
        true_alternative_index: int,
        created_at: datetime.datetime = None,
        created_by: str = None,
        order_matters: bool = False,
    ) -> None:
        """
        2 or more probabilities are required. Make sure that they sum to 100.
        """
        assert sum(probabilities) == 100, "Probabilities need to sum to 100."
        length = len(probabilities)
        assert length >= 2, "A prediction needs at least two probabilities."
        assert (
            true_alternative_index >= 0
        ), "The true alternative index cannot be negative"
        assert (
            true_alternative_index <= length - 1
        ), "Probabilities need to contain the true alternative"
        self.created_at = created_at
        self.created_by = created_by
        if created_at:
            self.created_on = created_at.date()
        self.order_matters = order_matters
        self.probabilities = probabilities
        self.true_alternative_index = true_alternative_index

    @property
    def brier_score(self) -> Decimal:
        if isinstance(self._cached_brier_score, Decimal):
            return self._cached_brier_score
        calculator: typing.Union[Brier, OrderedCategorical] = (
            OrderedCategorical(true_alternative_index=self.true_alternative_index)
            if self.order_matters
            else Brier(true_alternative_index=self.true_alternative_index)
        )
        score = calculator.calculate(self)
        self._cached_brier_score = score
        return score


def compare(
    predictions: typing.Tuple[Prediction, ...]
) -> typing.Tuple[Decimal, typing.Tuple[Prediction, ...]]:
    brier_scores: typing.List[Decimal] = []
    for prediction in predictions:
        brier_scores.append(prediction.brier_score)
    median = Decimal(statistics.median(brier_scores))
    enriched_predictions: typing.List[Prediction] = []
    for prediction in predictions:
        prediction.relative_brier_score = prediction.brier_score - median
        enriched_predictions.append(prediction)
    return median, tuple(enriched_predictions)


class Day:
    scores: typing.Dict[str, Decimal] = {}
    creators: typing.List[str] = []
    date: datetime.date
    predictions: typing.List[Prediction]
    scored_predictions: typing.Tuple[Prediction]
    median: Decimal

    def __init__(
        self, date: datetime.date, predictions: typing.List[Prediction]
    ) -> None:
        self.date = date
        self.predictions = predictions
        latest_predictions: typing.List[Prediction] = []
        for prediction in predictions:
            if prediction.created_by not in self.creators:
                self.creators.append(prediction.created_by)
        for creator in self.creators:
            creator_predictions: typing.List[Prediction] = []
            for _prediction in predictions:
                if _prediction.created_by == creator:
                    creator_predictions.append(_prediction)
            if len(creator_predictions) == 0:
                continue
            latest_prediction = creator_predictions[0]
            for creator_prediction in creator_predictions:
                if creator_prediction.created_at > latest_prediction.created_at:
                    latest_prediction = creator_prediction
            latest_predictions.append(latest_prediction)
        (self.median, self.scored_predictions) = compare(tuple(latest_predictions))
        for scored_prediction in self.scored_predictions:
            self.scores[
                scored_prediction.created_by
            ] = scored_prediction.relative_brier_score


class Timeline:
    scores: typing.Dict[str, Decimal] = {}
    days: typing.List[Day]

    def __init__(self, predictions: typing.FrozenSet[Prediction]) -> None:
        dates: typing.List[datetime.date] = []
        creators: typing.List[str] = []
        for prediction in predictions:
            created_on = prediction.created_on
            if created_on not in dates:
                dates.append(created_on)
            creator = prediction.created_by
            if creator not in creators:
                creators.append(creator)
        creators.sort()
        dates.sort()
        days: typing.List[Day] = []
        first_date = dates[0]
        last_date = dates[1]
        date = first_date
        while date <= last_date:
            prediction_found = False
            for prediction in predictions:
                if prediction.created_on == date:
                    prediction_found = True
            if prediction_found:
                date_predictions: typing.List[Prediction] = []
                for prediction in predictions:
                    if prediction.created_on == date:
                        prediction_found = True
                        date_predictions.append(prediction)
                day = Day(date, date_predictions)
            if "day" in locals():
                days.append(day)
            date = date + datetime.timedelta(days=1)
        self.days = days
        nominators: typing.Dict[str, Decimal] = {}
        for creator in creators:
            nominators[creator] = Decimal(0)
        for day in days:
            for creator, score in day.scores.items():
                nominators[creator] = nominators[creator] + score
        denominator = len(days)
        for creator, nominator in nominators.items():
            self.scores[creator] = nominator / denominator
