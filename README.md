![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)
![tests](https://github.com/yhoiseth/python-prediction-scorer/workflows/tests/badge.svg)

# Python Prediction Scorer

The purpose of this library is to help you score and compare predictions.

## Status

Python Prediction Scorer is neither stable nor feature complete. Expect major backwards-incompatible changes.

## Goals

With this library, I aim to correctly implement many useful prediction scoring rules in a library that is user-friendly and easy to maintain and improve.

## Background

Some of the code in this library comes from my work at [Empiricast](https://yngve.hoiseth.net/empiricast-post-mortem/), a forecasting startup I co-founded.

For a thorough introduction to scoring rules, see [Calibration Scoring Rules for Practical Prediction Training](https://arxiv.org/abs/1808.07501v1) by [Spencer Greenberg](https://www.spencergreenberg.com/).

## Installation

`pip install predictionscorer`

### System requirements

Python Prediction Scorer requires Python 3.7+. There are currently no other dependencies.

## Usage

For example, say that George and Kramer were predicting the outcome of the 2016 US presidential election. George said that Donald Trump had a 40 percent probability of winning, while Kramer put Trump’s chances at 65 percent.

Considering that Trump won, Kramer’s prediction was better than George’s. But how much better? In order to find out, we must quantify the quality of their predictions. That’s what this library does.

There are several ways to score predictions like these. Here, we are using [Brier scores](https://www.gjopen.com/faq#faq4). Below, you can see a chart of what the Brier score would be given a range of different probabilities for the alternative that turned out to be true.

![Brier scores for probabilities 0-100](docs/images/brier-scores-probabilities-0-100.svg)

(See [plot.py](plot.py) for the code that generated this chart.)

Now, back to our election example. The following code scores the predictions using the Brier scoring rule.

```python
from decimal import Decimal

import predictionscorer

true_alternative_index = 1 # Alternative 0 is Hillary Clinton. Alternative 1 is Donald Trump.

george = predictionscorer.Prediction(
    probabilities=(Decimal(60), Decimal(40)), # George put Clinton at 60 % and Trump at 40 %.
    true_alternative_index=true_alternative_index,
)

print(george.brier_score) # Decimal('0.72')

kramer = predictionscorer.Prediction(
    probabilities=(Decimal(35), Decimal(65)), # Kramer put Clinton at 35 % and Trump at 65 %.
    true_alternative_index=true_alternative_index,
)

print(kramer.brier_score) # Decimal('0.245')
```

As you can see, Kramer’s score is _lower_ than George’s. How can a better prediction give a lower score? The thing is, with Brier scores, the lower, the better. To help your intuition, you can consider a Brier score as the _distance from the truth_. (A perfect prediction yields 0, while the worst possible prediction yields 2.)

### More than two alternatives

The above example is binary — there are only two alternatives. But sometimes you need more. For example, you might want to add an “other” alternative:

```python
from decimal import Decimal

import predictionscorer

prediction = predictionscorer.Prediction(
    probabilities=(
        Decimal(55), # Clinton
        Decimal(35), # Trump
        Decimal(10), # Other
    ),
    true_alternative_index=1,
)

print(prediction.brier_score) # Decimal('0.735')
```

#### If the order matters

Sometimes, the ordering of alternatives matters. For example, consider the following question:

> What will the closing value of the S&P 500 stock market index be on 2019-12-31?
>
> | Index | Alternative                                  |
> |-------|----------------------------------------------|
> | 0     | < 3,000.00                                   |
> | 1     | ≥ 3,000.00, < 3,500.00                       |
> | 2     | ≥ 3,500.00, < 4,000.00                       |
> | 3     | ≥ 4,000.00                                   |

We [now know that the answer is 3,230.78](https://us.spindices.com/indices/equity/sp-500). This means that, among our alternatives, the one with index 1 turned out to be correct. But notice that index 2 is closer to the right answer than index 3. In such cases, the regular Brier score is a poor measure of forecasting accuracy. Instead, we can use [the ordered categorical scoring rule](https://goodjudgment.io/Training/Ordered_Categorical_Scoring_Rule.pdf).

The code below should look familiar, except that we are now setting `order_matters=True`:

```python
from decimal import Decimal

import predictionscorer

prediction = predictionscorer.Prediction(
    probabilities=(
        Decimal(25),
        Decimal(25),
        Decimal(30),
        Decimal(20),
    ),
    true_alternative_index=1,
    order_matters=True,
)

print(prediction.brier_score) # Decimal('0.2350')
```

## Comparing scores

So far, we have looked at how to score predictions on an _absolute_ scale. Now, let’s compare them to each other:

```python
from decimal import Decimal

import predictionscorer

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

print(median) # Decimal('0.4825') 
print(george.relative_brier_score) # Decimal('0.2375')
print(kramer.relative_brier_score) # Decimal('-0.2375')
```

As you can see, George’s score is 0.2375 higher (worse) than the median, whilst Kramer’s score is 0.2375 lower (better).

### Comparing scores over time

It is more difficult to predict things a long time into the future. It is also more valuable to have good predictions farther in advance. Also, predictions can often be updated over time. To account for these things, we can do the following. 

1. Group predictions by date. If one person (or bot) made several predictions in any given day, discard all but the most recent one. If someone doesn’t make a forecast on any given day, use their most recent forecast from previous days.
2. Score the forecasts against each other within each day.
3. Average all the relative scores to get the total relative score.

#### Example

To illustrate, consider the following six (made-up) predictions for the 2016 US presidential election. In this example, no forecasts could be made after November 7.

| ID | Forecaster | Clinton | Trump | Date       | Time  |
|----|------------|---------|-------|------------|-------|
| 1  | George     | 70      | 30    | Nov 1      | 16:05 |
| 2  | Kramer     | 40      | 60    | Nov 2      | 11:37 |
| 3  | George     | 50      | 50    | Nov 3      | 09:09 |
| 4  | George     | 60      | 40    | Nov 3      | 21:42 |
| 5  | Kramer     | 30      | 70    | Nov 5      | 11:45 |

```python
import datetime
from decimal import Decimal

import predictionscorer

KRAMER = "Kramer"
GEORGE = "George"

# Dump the set of predictions into the a new Timeline object:
timeline = predictionscorer.Timeline({
    predictionscorer.Prediction(
        (Decimal(70), Decimal(30)), 
        true_alternative_index=1, 
        created_at=datetime.datetime(2016, 11, 1, 16, 5), 
        created_by=GEORGE,
    ),
    predictionscorer.Prediction(
        (Decimal(40), Decimal(60)), 
        true_alternative_index=1, 
        created_at=datetime.datetime(2016, 11, 2, 11, 37), 
        created_by=KRAMER,
    ),
    predictionscorer.Prediction(
        (Decimal(50), Decimal(50)), 
        true_alternative_index=1, 
        created_at=datetime.datetime(2016, 11, 3, 9, 9), 
        created_by=GEORGE,
    ),
    predictionscorer.Prediction(
        (Decimal(60), Decimal(40)), 
        true_alternative_index=1, 
        created_at=datetime.datetime(2016, 11, 3, 21, 42), 
        created_by=GEORGE,
    ),
    predictionscorer.Prediction(
        (Decimal(30), Decimal(70)), 
        true_alternative_index=1, 
        created_at=datetime.datetime(2016, 11, 5, 11, 45), 
        created_by=KRAMER,
    ),
})

# We can now access a dictionary of creators to get their relative Brier scores:
print(timeline.creators[GEORGE]) # Decimal('')
print(timeline.creators[KRAMER]) # Decimal('')

# We can also access an ordered dictionary of days:
november_5 = timeline.days[datetime.date(2016, 11, 1)]
print(november_5.median) # Decimal('')

# Each day contains a dictionary of the predictions that counted. The key is the user, so you can get their scores that day:
print(november_5.creators[GEORGE].brier_score) # Decimal('')
print(november_5.creators[GEORGE].relative_brier_score) # Decimal('')

# Days also have a median Brier score property:
print(november_5.median_brier_score) # Decimal('')
```

## Changelog

See [CHANGELOG.md](CHANGELOG.md).

## Goals and judgment calls

With this library, I am trying to achieve the following goals.

- Feature complete
- Easy to read (for as many people as possible)
- Easy and predictable to use (with modern tools)

### Feature complete

There are many ways to score and compare predictions, some more complicated than others. For example, consider the case where many people make multiple forecasts on the same question over a period of time. We want to award being right early, which means comparing early forecasts to early forecasts, late forecasts to late forecasts, and aggregating them all together.

The library should handle even such advanced cases.

### Easy to read (for as many people as possible)

The code should be easy to read, even for people who don’t know math or Python well. 

To achieve this, I’ve opted for an object-oriented design rather than, say, the array approach used by [NumPy](https://numpy.org/). The result is a more verbose and explicit API. I also try to not use advanced Python features (which many don’t understand).

### Easy and predictable to use (with modern tools)

The library should be easy to use, and the results should be predictable and correct.

- Type hints and annotations wherever possible (this also makes the code easier to read). Use a modern IDE like [PyCharm](https://www.jetbrains.com/pycharm/) and/or a type checker like [mypy](http://mypy-lang.org/) to benefit from this.
- The [Decimal](https://docs.python.org/3/library/decimal.html) data type rather than floats. This makes the library a bit more involved to use if you don’t use decimals in your code, but you won’t get unexpected return values like 3.3000000000000003.
- Assertions so the code fails early instead of producing incorrect results. For example, creating an instance of the `Prediction` class will fail if you pass it probabilities that sum to anything else than 100.
- Probabilities as percentages, not decimals. Most people think in terms of percentages, not decimals — e.g., “50 % likely,” not “0.50 likely.”
- Automated tests to make sure that we get the expected results.
- Immutability where possible in order to prevent bugs.
- [Semantic versioning](https://semver.org/) in order to make it easy to deal with changes.

## Issues

Please [open an issue on GitHub](https://github.com/yhoiseth/python-prediction-scorer/issues/new) if you discover any problems or potential for improvement.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).
