import math
from typing import Union


def brier_score(probability: Union[float, int]) -> float:
    """Calculate the Brier score for the provided probability.

    Parameters
    ----------
    probability
        A number greater than or equal to 0 and less than or equal to 1.

    Returns
    -------
    float
        From 2 (worst) to 0 (best).

    Raises
    ------
    AssertionError
        If `probability` is less than 0 or greater than 1.
    """
    _assert_valid_probability(probability)
    return _round(2 * (_inverse_probability(probability) ** 2))


def _assert_valid_probability(probability: Union[float, int]) -> None:
    assert (
        probability >= 0
    ), "A probability cannot be less than zero, as a probability of zero indicates absolute certainty."
    assert (
        probability <= 1
    ), "A probability cannot be greater than one, as a probability of one indicates absolute certainty."


def logarithmic_score(probability: Union[float, int]) -> float:
    """Calculate the logarithmic score for the provided probability.

    Parameters
    ----------
    probability
        A number greater than 0 and less than or equal to 1.

    Returns
    -------
    float
        Approaches infinity as `probability` approaches zero. The best possible score is 0.

    Raises
    ------
    AssertionError
        If `probability` is less than or equal to 0 or greater than 1.
    """
    _assert_valid_probability(probability)
    assert (
        probability != 0
    ), "The logarithmic score of zero is not defined because the logarithm of zero is not defined."
    return _round(-_log(probability))


def practical_score(
    probability: Union[float, int],
    max_probability: Union[float, int] = 1,
    max_score: Union[float, int] = 2,
) -> float:
    """Calculate the practical score for the provided probability.

    Parameters
    ----------
    probability
        A number greater than 0 and less than or equal to `max_probability`.
    max_probability
        The maximum probability allowed. Defaults to 1.
    max_score
        The maximum score allowed. Defaults to 2.

    Returns
    -------
    float
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
    _assert_valid_practical_score_inputs(probability, max_probability, max_score)
    nominator = max_score * (_log(probability) + 1)
    denominator = _log(max_probability + 1)
    score = nominator / denominator
    if score > max_score:
        score = max_score
    return _round(score)


def quadratic_score(probability: Union[float, int]) -> float:
    """Calculate the quadratic score for the provided probability.

    Parameters
    ----------
    probability
        A number greater than or equal to 0 and less than or equal to 1.

    Returns
    -------
    float
        The worst possible score is -1. The best possible score is 1.

    Raises
    ------
    AssertionError
        If `probability` is less than 0 or greater than 1.
    """
    _assert_valid_probability(probability)
    inverse = _inverse_probability(probability)
    return _round(probability * (2 - probability) - inverse ** 2)


def _assert_valid_practical_score_inputs(
    probability: Union[float, int],
    max_probability: Union[float, int],
    max_score: Union[float, int],
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


def _inverse_probability(probability: Union[float, int]) -> float:
    return float(1 - probability)


def _log(value: Union[float, int]) -> float:
    return float(math.log2(value))


def _round(score: float) -> float:
    return float(f"{score:.2f}")
