from decimal import Decimal
from typing import List

from matplotlib import pyplot as plt

from predictionscorer.choice import Prediction

predictions: List[Prediction] = []
x_axis_data: List[int] = []
for index in range(1, 100):
    predictions.append(Prediction(index / 100, Decimal(2)))
    x_axis_data.append(index)

y_axis_data: List[Decimal] = []

for prediction in predictions:
    y_axis_data.append(prediction.brier)

plt.plot(x_axis_data, y_axis_data)
plt.xlabel("Probability assigned to correct answer")
plt.ylabel("Brier score")
plt.title("Brier score for probabilities 1 % - 99 %")
plt.draw()
plt.savefig("docs/charts/choice/brier.svg")

plt.clf()

y_axis_data = []

for prediction in predictions:
    y_axis_data.append(prediction.logarithmic)

plt.plot(x_axis_data, y_axis_data)
plt.xlabel("Probability assigned to correct answer")
plt.ylabel("Logarithmic score")
plt.title("Logarithmic score for probabilities 1 % - 99 %")
plt.draw()
plt.savefig("docs/charts/choice/logarithmic.svg")

plt.clf()

y_axis_data = []

for prediction in predictions:
    y_axis_data.append(prediction.practical)

plt.plot(x_axis_data, y_axis_data)
plt.xlabel("Probability assigned to correct answer")
plt.ylabel("Practical score")
plt.title("Practical score for probabilities 1 % - 99 %")
plt.draw()
plt.savefig("docs/charts/choice/practical.svg")

plt.clf()

y_axis_data = []

for prediction in predictions:
    y_axis_data.append(prediction.quadratic)

plt.plot(x_axis_data, y_axis_data)
plt.xlabel("Probability assigned to correct answer")
plt.ylabel("Quadratic score")
plt.title("Quadratic score for probabilities 1 % - 99 %")
plt.draw()
plt.savefig("docs/charts/choice/quadratic.svg")
