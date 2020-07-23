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
for index in range(1, 100):
    probabilities.append((index / 100))

y_axis_data: List[Decimal] = []

for probability in probabilities:
    y_axis_data.append(brier_score(probability))

plt.plot(probabilities, y_axis_data)
plt.xlabel("Probability assigned to correct answer")
plt.ylabel("Brier score")
plt.draw()
plt.savefig("docs/charts/brier.svg")

plt.clf()

y_axis_data = []

for probability in probabilities:
    y_axis_data.append(logarithmic_score(probability))

plt.plot(probabilities, y_axis_data)
plt.xlabel("Probability assigned to correct answer")
plt.ylabel("Logarithmic score")
plt.draw()
plt.savefig("docs/charts/logarithmic.svg")

plt.clf()

y_axis_data = []

for probability in probabilities:
    y_axis_data.append(practical_score(probability))

plt.plot(probabilities, y_axis_data)
plt.xlabel("Probability assigned to correct answer")
plt.ylabel("Practical score")
plt.draw()
plt.savefig("docs/charts/practical.svg")

plt.clf()

y_axis_data = []

for probability in probabilities:
    y_axis_data.append(quadratic_score(probability))

plt.plot(probabilities, y_axis_data)
plt.xlabel("Probability assigned to correct answer")
plt.ylabel("Quadratic score")
plt.draw()
plt.savefig("docs/charts/quadratic.svg")
