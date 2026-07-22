# Welcome to PyStatPower

**PyStatPower** is a modern, streamlined Python package tailored for statistical power analysis, sample size estimation, power calculation, and effect size solving.

Built with precision and developer experience in mind, it bridges the gap between statistical rigor and clean, pythonic interfaces.

---

## ✨ Key Features

- **🎯 Comprehensive Testing Frameworks**: Supports Inequality, Non-Inferiority, Superiority, and Equivalence (TOST) tests.
- **⚡ Flexible Solvers**: Effortlessly solve for sample sizes, statistical power, or effect sizes.
- **🐍 Pythonic & Modern**: Intuitive namespace design (`proportion.single.inequality...`), fully typed, and compatible with Python 3.10+.
- **⚙️ Minimal Dependencies**: Built directly on top of SciPy without heavy framework overhead.
- **🧪 Rigorously Tested**: Verified across multiple SciPy and Python release matrix combinations.

---

## 🚀 Quick Example

Estimating the required sample size for a **Two-Sample Non-Inferiority Trial** takes only a few lines of code:

```python
from pystatpower import proportion

# Estimate sample size for non-inferiority proportion test
treatment_size, reference_size = proportion.independent.noninferiority.solve_size(
    treatment_proportion=0.95,
    reference_proportion=0.90,
    margin=-0.10,
    alternative="greater",
    alpha=0.025,
    power=0.8,
)

print(f"Required Sample Size: Treatment={treatment_size}, Reference={reference_size}")
# Output: Required Sample Size: Treatment=48, Reference=48
```

---

## 🧩 Package Architecture & API Reference

`PyStatPower` offers a clean, hierarchical API design divided into four core statistical domains.

Each domain provides dedicated submodules for confidence intervals (`ci`), inequality/difference tests (`inequality`),
non-inferiority (`noninferiority`), superiority (`superiority`), and equivalence (`equivalence`).

```text
pystatpower
├── mean            # Mean Models (Single, Independent, Paired)
├── proportion      # Proportion Models (Single, Independent, Paired)
├── correlation     # Correlation Models
└── misc            # Specialized Models
```

👉 **Explore the full function signatures and parameter details in our [API Reference](api/index.md).**

---

## 🔗 Useful Links

- 🗺️ [Project Roadmap & Status](./roadmap.md) — Check supported statistical models and future feature plans.
- 📦 [PyPI Releases](https://pypi.org/project/pystatpower/) — Package downloads and version history.
- 🛠️ [GitHub Repository](https://github.com/Snoopy1866/pystatpower) — Source code, issue tracker, and contributions.
