from decimal import Decimal
from typing import List

from matplotlib import pyplot as plt

from predictionscorer.rules import (
    brier_score,
    logarithmic_score,
    practical_score,
    quadratic_score,
)

probabilities: List[float] = []
x_axis_data: List[int] = []
for index in range(1, 100):
    probabilities.append((index / 100))
    x_axis_data.append(index)

y_axis_data: List[Decimal] = []

for probability in probabilities:
    y_axis_data.append(brier_score(probability))

plt.plot(x_axis_data, y_axis_data)
plt.xlabel("Probability assigned to correct answer")
plt.ylabel("Brier score")
plt.title("Brier score for probabilities 1 % - 99 %")
plt.draw()
plt.savefig("docs/charts/brier.svg")

plt.clf()

y_axis_data = []

for probability in probabilities:
    y_axis_data.append(logarithmic_score(probability))

plt.plot(x_axis_data, y_axis_data)
plt.xlabel("Probability assigned to correct answer")
plt.ylabel("Logarithmic score")
plt.title("Logarithmic score for probabilities 1 % - 99 %")
plt.draw()
plt.savefig("docs/charts/logarithmic.svg")

plt.clf()

y_axis_data = []

for probability in probabilities:
    y_axis_data.append(practical_score(probability))

plt.plot(x_axis_data, y_axis_data)
plt.xlabel("Probability assigned to correct answer")
plt.ylabel("Practical score")
plt.title("Practical score for probabilities 1 % - 99 %")
plt.draw()
plt.savefig("docs/charts/practical.svg")

plt.clf()

y_axis_data = []

for probability in probabilities:
    y_axis_data.append(quadratic_score(probability))

plt.plot(x_axis_data, y_axis_data)
plt.xlabel("Probability assigned to correct answer")
plt.ylabel("Quadratic score")
plt.title("Quadratic score for probabilities 1 % - 99 %")
plt.draw()
plt.savefig("docs/charts/quadratic.svg")
