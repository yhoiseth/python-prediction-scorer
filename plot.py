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
for index in range(0, 101):
    probabilities.append((index / 100))

y_axis_data: List[Decimal] = []

for probability in probabilities:
    y_axis_data.append(brier_score(probability))

plt.plot(probabilities, y_axis_data)
plt.xlabel("Probability assigned to correct answer")
plt.xticks([0.0, 0.25, 0.50, 0.75, 1.0])
# plt.yticks([0.0, 0.50, 1.0, 1.5, 2.0])
plt.grid(True)
plt.ylabel("Brier score")
plt.draw()
plt.savefig("docs/charts/brier.svg")

plt.clf()

y_axis_data = []

for probability in probabilities:
    y_axis_data.append(quadratic_score(probability))

plt.plot(probabilities, y_axis_data)
plt.xlabel("Probability assigned to correct answer")
plt.xticks([0.0, 0.25, 0.50, 0.75, 1.0])
# plt.yticks([-1.0, -0.50, 0, 0.5, 1.0])
plt.grid(True)
plt.ylabel("Quadratic score")
plt.draw()
plt.savefig("docs/charts/quadratic.svg")

plt.clf()

probabilities.pop(0)

y_axis_data = []
for probability in probabilities:
    y_axis_data.append(practical_score(probability, max_probability=1))

plt.plot(probabilities, y_axis_data)
plt.xlabel("Probability assigned to correct answer")
plt.xticks([0.0, 0.25, 0.50, 0.75, 1.0])
plt.grid(True)
plt.ylabel("Practical score")
plt.draw()
plt.savefig("docs/charts/practical.svg")

plt.clf()

y_axis_data = []

for probability in probabilities:
    y_axis_data.append(logarithmic_score(probability))

plt.plot(probabilities, y_axis_data)
plt.xlabel("Probability assigned to correct answer")
plt.xticks([0.0, 0.25, 0.50, 0.75, 1.0])
plt.grid(True)
plt.ylabel("Logarithmic score")
plt.draw()
plt.savefig("docs/charts/logarithmic.svg")
