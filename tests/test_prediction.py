import datetime
from decimal import Decimal

import pytest

import predictionscorer


class TestInitialization:
    def test_probabilities_count(self):
        with pytest.raises(AssertionError) as assertion_error:
            predictionscorer.Prediction(
                probabilities=(Decimal("100"),), true_alternative_index=0
            )
        assert "A prediction needs at least two probabilities." in str(
            assertion_error.value
        )

    def test_probabilities_sum_more_than_100(self):
        with pytest.raises(AssertionError) as assertion_error:
            predictionscorer.Prediction(
                probabilities=(Decimal("75"), Decimal("25.01"),),
                true_alternative_index=0,
            )
        assert "Probabilities need to sum to 100." in str(assertion_error.value)

    def test_probabilities_sum_less_than_100(self):
        with pytest.raises(AssertionError) as assertion_error:
            predictionscorer.Prediction(
                probabilities=(Decimal("75"), Decimal("24.99"),),
                true_alternative_index=1,
            )
        assert "Probabilities need to sum to 100." in str(assertion_error.value)

    def test_true_alternative_index_not_in_probabilities(self):
        with pytest.raises(AssertionError) as assertion_error:
            predictionscorer.Prediction(
                probabilities=(Decimal("75"), Decimal("25"),), true_alternative_index=2
            )
        assert "Probabilities need to contain the true alternative" in str(
            assertion_error.value
        )

    def test_negative_true_alternative_index(self):
        with pytest.raises(AssertionError) as assertion_error:
            predictionscorer.Prediction(
                probabilities=(Decimal("75"), Decimal("25"),), true_alternative_index=-1
            )
        assert "The true alternative index cannot be negative" in str(
            assertion_error.value
        )


class TestBrier:
    def test_60_40_with_cache(self):
        prediction = predictionscorer.Prediction(
            probabilities=(Decimal(60), Decimal(40),), true_alternative_index=1,
        )
        assert prediction._cached_brier_score is None
        score = prediction.brier_score
        assert score == prediction._cached_brier_score
        assert score == Decimal("0.72")

    def test_35_65(self):
        prediction = predictionscorer.Prediction(
            probabilities=(Decimal(35), Decimal(65),), true_alternative_index=1,
        )
        assert prediction.brier_score == Decimal("0.245")

    def test_readme_example_more_than_two_alternatives(self):
        prediction = predictionscorer.Prediction(
            probabilities=(Decimal(55), Decimal(35), Decimal(10),),
            true_alternative_index=1,
        )
        assert prediction.brier_score == Decimal("0.735")

    def test_order_matters(self):
        prediction = predictionscorer.Prediction(
            probabilities=(Decimal(25), Decimal(25), Decimal(30), Decimal(20),),
            true_alternative_index=1,
            order_matters=True,
        )
        assert prediction.brier_score == Decimal("0.2350")


class TestComparison:
    def test_two_binary_predictions(self):
        true_alternative_index = 1
        george = predictionscorer.Prediction(
            probabilities=(Decimal(60), Decimal(40)),
            true_alternative_index=true_alternative_index,
        )
        kramer = predictionscorer.Prediction(
            probabilities=(Decimal(35), Decimal(65)),
            true_alternative_index=true_alternative_index,
        )

        (median, (george, kramer)) = predictionscorer.compare((george, kramer))

        assert median == Decimal("0.4825")
        assert george.relative_brier_score == Decimal("0.2375")
        assert kramer.relative_brier_score == Decimal("-0.2375")


class TestInitializeQuestion:
    def test(self):
        GEORGE = "George"
        KRAMER = "Kramer"
        predictions = (
            predictionscorer.AttributedPrediction(
                (Decimal(70), Decimal(30)),
                true_alternative_index=1,
                created_at=datetime.datetime(2016, 11, 1, 16, 5),
                forecaster_id=GEORGE,
            ),
            predictionscorer.AttributedPrediction(
                (Decimal(40), Decimal(60)),
                true_alternative_index=1,
                created_at=datetime.datetime(2016, 11, 2, 11, 37),
                forecaster_id=KRAMER,
            ),
            predictionscorer.AttributedPrediction(
                (Decimal(50), Decimal(50)),
                true_alternative_index=1,
                created_at=datetime.datetime(2016, 11, 3, 9, 9),
                forecaster_id=GEORGE,
            ),
            predictionscorer.AttributedPrediction(
                (Decimal(60), Decimal(40)),
                true_alternative_index=1,
                created_at=datetime.datetime(2016, 11, 3, 21, 42),
                forecaster_id=GEORGE,
            ),
            predictionscorer.AttributedPrediction(
                (Decimal(30), Decimal(70)),
                true_alternative_index=1,
                created_at=datetime.datetime(2016, 11, 5, 11, 45),
                forecaster_id=KRAMER,
            ),
        )

        question = predictionscorer.Question(
            predictions, datetime.date(2016, 11, 1), datetime.date(2016, 11, 7)
        )

        dates = question.dates
        assert len(dates) == 7
        assert dates[0] == datetime.date(2016, 11, 1)
        assert dates[1] == datetime.date(2016, 11, 2)
        assert dates[2] == datetime.date(2016, 11, 3)
        assert dates[3] == datetime.date(2016, 11, 4)
        assert dates[4] == datetime.date(2016, 11, 5)
        assert dates[5] == datetime.date(2016, 11, 6)
        assert dates[6] == datetime.date(2016, 11, 7)

        forecasters = question.forecasters
        assert len(forecasters) == 2
        george = forecasters[0]
        kramer = forecasters[1]
        assert george.id == GEORGE
        assert kramer.id == KRAMER
        assert george.participation_rate == Decimal("1")
        assert kramer.participation_rate == pytest.approx(Decimal("0.8571428"))
        assert george.average_daily_brier_score == pytest.approx(Decimal("0.7942857"))
        assert kramer.average_daily_brier_score == Decimal("0.25")
        assert george.accuracy_score == Decimal("0.22")
        assert kramer.accuracy_score == pytest.approx(Decimal("-0.3783333"))

        days = question.days
        assert len(days) == 7
        assert days[0].median_brier_score == Decimal("0.98")
        assert days[1].median_brier_score == Decimal("0.65")
        assert days[2].median_brier_score == Decimal("0.52")
        assert days[3].median_brier_score == Decimal("0.52")
        assert days[4].median_brier_score == Decimal("0.45")
        assert days[5].median_brier_score == Decimal("0.45")
        assert days[6].median_brier_score == Decimal("0.45")

        assert question.average_median_daily_brier_score == pytest.approx(
            Decimal("0.5742857")
        )


class TestDateRangeGenerator:
    def test(self):
        GEORGE = "George"
        KRAMER = "Kramer"
        actual_date_range = predictionscorer.generate_date_range(
            (
                predictionscorer.AttributedPrediction(
                    (Decimal(70), Decimal(30)),
                    true_alternative_index=1,
                    created_at=datetime.datetime(2016, 11, 1, 16, 5),
                    forecaster_id=GEORGE,
                ),
                predictionscorer.AttributedPrediction(
                    (Decimal(40), Decimal(60)),
                    true_alternative_index=1,
                    created_at=datetime.datetime(2016, 11, 2, 11, 37),
                    forecaster_id=KRAMER,
                ),
                predictionscorer.AttributedPrediction(
                    (Decimal(50), Decimal(50)),
                    true_alternative_index=1,
                    created_at=datetime.datetime(2016, 11, 3, 9, 9),
                    forecaster_id=GEORGE,
                ),
                predictionscorer.AttributedPrediction(
                    (Decimal(60), Decimal(40)),
                    true_alternative_index=1,
                    created_at=datetime.datetime(2016, 11, 3, 21, 42),
                    forecaster_id=GEORGE,
                ),
                predictionscorer.AttributedPrediction(
                    (Decimal(30), Decimal(70)),
                    true_alternative_index=1,
                    created_at=datetime.datetime(2016, 11, 5, 11, 45),
                    forecaster_id=KRAMER,
                ),
            )
        )
        expected_date_range = (
            datetime.date(2016, 11, 1),
            datetime.date(2016, 11, 2),
            datetime.date(2016, 11, 3),
            datetime.date(2016, 11, 4),
            datetime.date(2016, 11, 5),
        )
        assert expected_date_range == actual_date_range


class TestEliminateOverwritten:
    def test(self):
        GEORGE = "George"
        KRAMER = "Kramer"
        with_overwritten = (
            predictionscorer.AttributedPrediction(
                (Decimal(70), Decimal(30)),
                true_alternative_index=1,
                created_at=datetime.datetime(2016, 11, 1, 16, 5),
                forecaster_id=GEORGE,
                _id="george_1",
            ),
            predictionscorer.AttributedPrediction(
                (Decimal(40), Decimal(60)),
                true_alternative_index=1,
                created_at=datetime.datetime(2016, 11, 2, 11, 37),
                forecaster_id=GEORGE,
                _id="george_2",
            ),
            predictionscorer.AttributedPrediction(
                (Decimal(60), Decimal(40)),
                true_alternative_index=1,
                created_at=datetime.datetime(2016, 11, 2, 21, 42),
                forecaster_id=GEORGE,
                _id="george_3",
            ),
            predictionscorer.AttributedPrediction(
                (Decimal(30), Decimal(70)),
                true_alternative_index=1,
                created_at=datetime.datetime(2016, 11, 5, 11, 45),
                forecaster_id=KRAMER,
                _id="kramer_1",
            ),
            predictionscorer.AttributedPrediction(
                (Decimal(50), Decimal(50)),
                true_alternative_index=1,
                created_at=datetime.datetime(2016, 11, 5, 9, 9),
                forecaster_id=KRAMER,
                _id="kramer_2",
            ),
        )
        relevant_ids = ["george_1", "george_3", "kramer_1"]
        eliminated = predictionscorer.eliminate_overwritten(with_overwritten)
        assert len(eliminated) == 3
        for prediction in eliminated:
            assert prediction.id in relevant_ids
