# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Added
- Changelog.
- Documentation and test for Brier calculation with more than two alternatives.
- Assertions for creating `Prediction` instances:
   - Two or more probabilities
   - Sum of probabilities must equal 100
- Calculation of scores for when the order of alternatives matters.

### Changed
- Decimal input for probabilities instead of integer.

## [0.1.1] - 2020-04-15
### Added
- Python version requirement (greater than or equal to 3.7) in `setup.py`.

### Fixed
- Inclusion of `README` on [PyPi project page](https://pypi.org/project/predictionscorer/).

## [0.1.0] - 2020-04-15
### Added
- Brier score calculation

[Unreleased]: https://github.com/yhoiseth/python-prediction-scorer/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/yhoiseth/python-prediction-scorer/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/yhoiseth/python-prediction-scorer/releases/tag/v0.1.0
