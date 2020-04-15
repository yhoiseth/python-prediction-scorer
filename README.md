![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)
![tests](https://github.com/yhoiseth/python-prediction-scorer/workflows/tests/badge.svg)

# Python Prediction Scorer

The purpose of this library is to help you compare predictions.

## Installation

`pip install predictionscorer` 

## Usage

For example, say that George and Kramer were predicting the outcome of the 2016 US presidential election. George said that Donald Trump had a 40 percent probability of winning, while Kramer put Trump's chances at 65 percent.

Considering that Trump won, Kramer's prediction was better than George's. But how much better? In order to find out, we must assign numerical scores to their predictions and compare them. That's what this library does.

The following code scores the predictions.

```python
from predictionscorer import calculators, predictions

george = predictions.Prediction(
    probabilities=[60, 40] # George put Clinton at 60 % and Trump at 40 %.
)
kramer = predictions.Prediction(
    probabilities=[35, 65] # Kramer put Clinton at 35 % and Trump at 65 %.
)

brier = calculators.Brier(
    true_alternative_index=1 # Alternative 0 is Hillary Clinton. Alternative 1 is Donald Trump.
)

print(brier.calculate(george)) # Decimal('0.72')
print(str(brier.calculate(kramer))) # '0.245'
```

As you can see, Kramer's score is _lower_ than George's. How can a better prediction give a lower score? The thing is, with Brier scores, the lower, the better. To help your intuition, you can consider a Brier score as the _distance from the truth_. (A perfect prediction yields 0, while the worst possible prediction yields 2.)

Questions where the order of alternatives matters is currently not supported.
