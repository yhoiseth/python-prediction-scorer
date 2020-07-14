from decimal import Decimal
from typing import Union

from predictionscorer._common import inverse_probability, log, to_decimal

_ONE = Decimal(1)
_TWO = Decimal(2)


def brier_score(probability: Union[Decimal, float, int]) -> Decimal:
    """Calculate the Brier score for the provided probability.

    Parameters
    ----------
    probability
        A number greater than or equal to 0 and less than or equal to 1.

    Returns
    -------
    Decimal
        From 2 (worst) to 0 (best).

    Raises
    ------
    AssertionError
        If `probability` is less than 0 or greater than 1.
    """
    probability = to_decimal(probability)
    _assert_valid_probability(probability)
    return _TWO * (inverse_probability(probability) ** _TWO)


def logarithmic_score(probability: Union[Decimal, float, int]) -> Decimal:
    """Calculate the logarithmic score for the provided probability.

    Parameters
    ----------
    probability
        A number greater than 0 and less than or equal to 1.

    Returns
    -------
    Decimal
        Approaches infinity as `probability` approaches zero. The best possible score is 0.

    Raises
    ------
    AssertionError
        If `probability` is less than or equal to 0 or greater than 1.
    """
    probability = to_decimal(probability)
    _assert_valid_probability(probability)
    assert (
        probability != 0
    ), "The logarithmic score of zero is not defined because the logarithm of zero is not defined."
    return -log(probability)


def practical_score(
    probability: Union[Decimal, float, int],
    max_probability: Union[Decimal, float, int] = Decimal("0.9999"),
    max_score: Union[Decimal, float, int] = _TWO,
) -> Decimal:
    """Calculate the practical score for the provided probability.

    Parameters
    ----------
    probability
        A number greater than 0 and less than or equal to `max_probability`.
    max_probability
        The maximum probability allowed. Defaults to 0.9999.
    max_score
        The maximum score allowed. Defaults to 2.

    Returns
    -------
    Decimal
        Approaches negative infinity as `probability` approaches 0. The best possible score (`probability` = 1) is defined by `max_score`.

    Raises
    ------
    AssertionError
        If `probability` is less than or equal to 0 or greater than `max_probability`.
    AssertionError
        If `max_score` is zero or less.
    AssertionError
        If `max_probability` is zero or less or greater than 1.
    """
    probability = to_decimal(probability)
    max_probability = to_decimal(max_probability)
    max_score = to_decimal(max_score)
    _assert_valid_practical_score_inputs(probability, max_probability, max_score)
    nominator = max_score * (log(probability) + _ONE)
    denominator = log(max_probability + _ONE)
    score = nominator / denominator
    if score > max_score:
        return max_score
    return score


def quadratic_score(probability: Union[Decimal, float, int]) -> Decimal:
    """Calculate the quadratic score for the provided probability.

    Parameters
    ----------
    probability
        A number greater than or equal to 0 and less than or equal to 1.

    Returns
    -------
    Decimal
        The worst possible score is -1. The best possible score is 1.

    Raises
    ------
    AssertionError
        If `probability` is less than 0 or greater than 1.
    """
    probability = to_decimal(probability)
    _assert_valid_probability(probability)
    inverse = inverse_probability(probability)
    return probability * (_TWO - probability) - inverse ** _TWO


def _assert_valid_practical_score_inputs(
    probability: Decimal, max_probability: Decimal, max_score: Decimal
) -> None:
    _assert_valid_probability(probability)
    _assert_valid_probability(max_probability)
    assert max_probability > 0, "max_probability must be greater than zero."
    assert (
        probability <= max_probability
    ), "probability cannot be greater than max_probability."
    assert max_score > 0, "max_score must be greater than zero."
    assert (
        probability != 0
    ), "The practical score of zero is not defined because the logarithm of zero is not defined."


def _assert_valid_probability(probability: Decimal) -> None:
    assert (
        probability >= 0
    ), "A probability cannot be less than zero, as a probability of zero indicates absolute certainty."
    assert (
        probability <= 1
    ), "A probability cannot be greater than one, as a probability of one indicates absolute certainty."
