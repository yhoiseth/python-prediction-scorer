![Code style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)

# Python Prediction Scorer

## Introduction

The purpose of this library is to help you _compare predictions_. Let's, for example, say that George and Kramer were predicting the outcome of the 2016 US presidential election. George said that Donald Trump had a 40 percent probability of winning, while Kramer put his chances at 65 percent.

Considering that Trump won, Kramer's prediction was better than George's. But how much better? In order to find out, we must assign numerical scores to their predictions and compare them. That's what this library does.

## Usage

```python
from predictionscorer.predictions import Prediction
from predictionscorer.calculators import Brier # Brier scoring is arguably the most common way of scoring predictions.

george = Prediction(probabilities=[60, 40]), # George put Clinton at 60 % and Trump at 40 %.
kramer = Prediction(probabilities=[35, 65]), # Kramer put Clinton at 35 % and Trump at 65 %.

calculator = Brier(true_alternative_index=1) # Alternative 0 is Hillary Clinton. Alternative 1 is Donald Trump.

print(Brier.calculate(george)) # 0.72
print(Brier.calculate(kramer)) # 0.245
```

As you can see, Kramer's score is _lower_ than George's. With Brier scores, the lower, the better. To help your intuition, you can consider a Brier score as the _distance from the truth_. (A perfect prediction yields 0, while the worst possible prediction yields 2.)

Only boolean questions (yes/no) are currently supported.
