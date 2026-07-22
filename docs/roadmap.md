# 🗺️ PyStatPower Roadmap

Welcome to the **PyStatPower** project roadmap! This document outlines the project's core vision, currently supported functionality, and planned future features.

> 💡 **Note**: This roadmap is a living document and will evolve as new features are implemented and community feedback is integrated.

## 🎯 Project Vision

`PyStatPower` aims to provide a lightweight, accurate, and easy-to-use Python toolkit for statistical power analysis, sample size estimation, power calculation, and effect size solving.

## 📚 Current Feature Status

Here is the current implementation status of statistical models in `PyStatPower`:

### 📊 Mean Models

- **Single Group**
  - [x] Confidence Interval
  - [x] Inequality Test
  - [x] Non-Inferiority Test
  - [x] Superiority Test
  - [ ] Equivalence Test

- **Two Independent Groups**
  - [x] Confidence Interval
  - [x] Inequality Test
  - [x] Non-Inferiority Test
  - [x] Superiority Test
  - [ ] Equivalence Test

- **Two Correlated Groups**
  - [ ] Confidence Interval
  - [ ] Inequality Test
  - [ ] Non-Inferiority Test
  - [ ] Superiority Test
  - [ ] Equivalence Test

### 🍰 Proportion Models

- **Single Group**
  - [x] Confidence Interval
  - [x] Inequality Test
  - [x] Non-Inferiority Test
  - [x] Superiority Test
  - [x] Equivalence Test

- **Two Independent Groups**
  - [x] Confidence Interval
  - [x] Inequality Test
  - [x] Non-Inferiority Test
  - [x] Superiority Test
  - [ ] Equivalence Test

- **Two Correlated Groups**
  - [ ] Confidence Interval
  - [ ] Inequality Test
  - [ ] Non-Inferiority Test
  - [ ] Superiority Test
  - [ ] Equivalence Test

### 📈 Correlation Models

- [x] Confidence Interval
- [x] Inequality Test

### 🧩 Miscellaneous Models

- [x] Observe At Least One Event
- [ ] Multi-Reader Multi-Case
- [ ] Bayesian Single-Arm Phase II Trial Designs with Time-to-Event Endpoints

## 🚀 Future Development Plans

### 🎯 Short-term Priorities

- [ ] Complete Equivalence Tests (TOST) for remaining Mean and Proportion models.
- [ ] Add support for Paired Samples in Mean and Proportion models.
- [ ] Improve exception handling and helpful error messages for edge parameter cases.

### 🔮 Mid-term Expansion

- [ ] **Survival Analysis**: Log-rank tests and Hazard Ratio power calculations.
- [ ] **ANOVA Models**: One-way and two-way ANOVA sample size estimations.

### 🌌 Long-term Vision

- [ ] Support advanced designs (e.g., Crossover trials, Repeated measures).
- [ ] Optional interactive Web UI for quick estimates without coding.

## 🤝 Contributing

Contributions are always welcome! If you would like to help build any of the features listed above, feel free to open a Pull Request or start a discussion in our Issues tracker.
