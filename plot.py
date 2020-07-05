from decimal import Decimal
from typing import List

import matplotlib.pyplot as plt

from predictionscorer.choice import Prediction

predictions: List[Prediction] = []
x_axis_data: List[int] = []
for index in range(1, 100):
    predictions.append(Prediction(index))
    x_axis_data.append(index)

y_axis_data: List[Decimal] = []

for prediction in predictions:
    y_axis_data.append(prediction.brier)

brier_plot = plt
brier_plot.plot(x_axis_data, y_axis_data)
brier_plot.xlabel("Probability")
brier_plot.ylabel("Brier score if true")
brier_plot.title("Brier scores for probabilities 0-100")
brier_plot.draw()
brier_plot.savefig("docs/charts/choice/brier.svg")
