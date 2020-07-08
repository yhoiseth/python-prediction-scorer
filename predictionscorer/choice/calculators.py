import math
from decimal import Decimal
from typing import Union

from predictionscorer.common import to_decimal

ONE = Decimal(1)
TWO = Decimal(2)


def inverse_probability(probability: Decimal) -> Decimal:
    return ONE - probability


def log(value: Decimal) -> Decimal:
    return Decimal(str(math.log2(value)))


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
    assert_valid_probability(probability)
    probability = to_decimal(probability)
    return TWO * (inverse_probability(probability) ** TWO)


def assert_valid_probability(probability: Union[Decimal, float, int]):
    assert (
        probability >= 0
    ), "A probability cannot be less than zero, as a probability of zero indicates absolute certainty."
    assert (
        probability <= 1
    ), "A probability cannot be greater than one, as a probability of one indicates absolute certainty."


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
    """
    assert_valid_probability(probability)
    assert (
        probability != 0
    ), "The logarithmic score of zero is not defined because the logarithm of zero is not defined."
    probability = to_decimal(probability)
    return -log(probability)


def practical_score(
    probability: Union[Decimal, float, int],
    max_probability: Union[Decimal, float, int],
    max_score: Union[Decimal, float, int],
) -> Decimal:
    probability = to_decimal(probability)
    max_probability = to_decimal(max_probability)
    max_score = to_decimal(max_score)
    nominator = max_score * (log(probability) + ONE)
    denominator = log(max_probability + ONE)
    score = nominator / denominator
    if score <= max_score:
        return score
    return max_score


def quadratic_score(probability: Union[Decimal, float, int]) -> Decimal:
    probability = to_decimal(probability)
    inverse = inverse_probability(probability)
    return probability * (TWO - probability) - inverse ** TWO
