<!-- markdownlint-disable MD024 -->

# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Fixed

- Marked as PEP 561 compatible

### Removed

## [1.0.0]

### Added

- New scoring rules API
- Charts for all scoring rules

### Changed

### Fixed

### Removed

- Old API

## [0.3.0] - 2020-05-24

### Added

- `compare` method to score predictions relative to each other
- Ability to import directly from `predictionscorer`
- `Question` class to score predictions over time
- MIT License

### Fixed

- Update [plot script](plot.py) to work with new API

## [0.2.0] - 2020-05-15

### Added

- Changelog.
- Documentation and test for Brier calculation with more than two alternatives.
- Assertions for creating `Prediction` instances:
  - Two or more probabilities
  - Sum of probabilities must equal 100
  - Probabilities must contain true alternative
- Calculation of scores for when the order of alternatives matters.
- Design philosophy documentation.
- Meta documentation
- API simplifications

### Changed

- Decimal input for probabilities instead of integer.
- Development tooling improvements (`pip-tools`).
- Tuples instead of lists for probabilities.

## [0.1.1] - 2020-04-15

### Added

- Python version requirement (greater than or equal to 3.7) in `setup.py`.

### Fixed

- Inclusion of `README` on [PyPi project page](https://pypi.org/project/predictionscorer/).

## [0.1.0] - 2020-04-15

### Added

- Brier score calculation.

[unreleased]: https://github.com/yhoiseth/python-prediction-scorer/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/yhoiseth/python-prediction-scorer/compare/v0.3.0...v1.0.0
[0.3.0]: https://github.com/yhoiseth/python-prediction-scorer/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/yhoiseth/python-prediction-scorer/compare/v0.1.1...v0.2.0
[0.1.1]: https://github.com/yhoiseth/python-prediction-scorer/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/yhoiseth/python-prediction-scorer/releases/tag/v0.1.0
