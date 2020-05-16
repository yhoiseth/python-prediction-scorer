import decimal
import typing

import matplotlib.pyplot as plt

from predictionscorer import predictions

all_predictions: typing.List[predictions.Prediction] = []

for index in range(0, 101):
    all_predictions.append(
        predictions.Prediction(
            (decimal.Decimal(index), decimal.Decimal(100 - index)),
            true_alternative_index=0,
        )
    )

x_axis_data: typing.List[decimal.Decimal] = []
y_axis_data: typing.List[decimal.Decimal] = []

for prediction in all_predictions:
    x_axis_data.append(prediction.probabilities[0])
    y_axis_data.append(prediction.brier_score)


plt.plot(x_axis_data, y_axis_data)
plt.xlabel("Probability")
plt.ylabel("Brier score if true")
plt.title("Brier scores for probabilities 0-100")
plt.draw()
plt.savefig("docs/images/brier-scores-probabilities-0-100.svg")
