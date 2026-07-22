# Contributing to PyStatPower

Thank you for your interest in contributing to **PyStatPower**! We welcome contributions of all kinds, including bug fixes, new statistical models, feature enhancements, documentation updates, and issue reports.

---

## 📜 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
  - [Reporting Bugs](#reporting-bugs)
  - [Suggesting Features](#suggesting-features)
  - [Adding Statistical Models](#adding-statistical-models)
- [Development Setup](#development-setup)
- [Development Workflow](#development-workflow)
  - [Code Style & Formatting](#code-style--formatting)
  - [Running Tests](#running-tests)
  - [Commit Message Guidelines](#commit-message-guidelines)
    - [Scope Naming Rules for Statistical Models](#scope-naming-rules-for-statistical-models)
- [Submitting a Pull Request (PR)](#submitting-a-pull-request-pr)

---

## 📜 Code of Conduct

By participating in this project, you agree to maintain a respectful, inclusive, and collaborative environment for everyone. Please treat fellow contributors with empathy and respect.

---

## 💡 How Can I Contribute?

### Reporting Bugs

If you encounter a bug or unexpected behavior:

1. Check the [Issue Tracker](https://github.com/Snoopy1866/pystatpower/issues) to ensure it hasn't already been reported.
2. Open a new issue with a clear title and description.
3. Include a **Minimal Reproducible Example (MRE)**, your Python version, SciPy version, and OS details.

### Suggesting Features

Ideas for new power analysis features or API improvements are always welcome! Please open an issue to discuss your proposal before implementing it.

### Adding Statistical Models

Check our roadmap in the README table for models marked as `⏳ WIP`. If you want to implement a missing model (e.g., equivalence tests for mean/proportion models):

- Ensure mathematical formulations and algorithms are reference-backed (e.g., PASS, SAS, or standard statistical literature). Please include references in code docstrings or PR descriptions.
- Implement methods for solving sample size (`solve_size`), power (`solve_power`), and, where applicable and feasible, effect size along with other relevant parameters.

---

## 🛠️ Development Setup

We use [`uv`](https://github.com/astral-sh/uv) for fast Python package management.

1. **Fork and clone the repository:**

   ```bash
   git clone https://github.com/Snoopy1866/pystatpower.git
   cd pystatpower
   ```

2. **Set up the virtual environment and install dependencies:**

   ```bash
   uv sync --all-groups
   ```

## 🔄 Development Workflow

### Code Style & Formatting

We strictly enforce code quality using [`ruff`](https://github.com/astral-sh/ruff).

- Format code:

  ```bash
  uv run ruff format
  ```

- Check for linting issues:

  ```bash
  uv run ruff check
  ```

### Running Tests

We use [pytest](https://github.com/pytest-dev/pytest) for testing. Please ensure all existing and new tests pass before opening a pull request.

- Run all unit tests:

  ```bash
  uv run pytest
  ```

- Run tests with coverage

  ```bash
  uv run pytest --cov=pystatpower
  ```

### Commit Message Guidelines

We follow the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification for all commit messages. This helps us generate automated changelogs and maintain a clean git history.

The commit message format should be:

```text
<type>(<scope>): <short description>
```

Common `<type>` prefixes include:

| Type       | Description                                                                                       |
| ---------- | ------------------------------------------------------------------------------------------------- |
| `feat`     | A new feature                                                                                     |
| `fix`      | A bug fix                                                                                         |
| `docs`     | Documentation only changes                                                                        |
| `style`    | Code style changes that do not affect logic (formatting, missing semicolons, etc.)                |
| `refactor` | A code change that neither fixes a bug nor adds a feature                                         |
| `perf`     | A code change that improves performance                                                           |
| `test`     | Adding missing tests or correcting existing tests                                                 |
| `build`    | Changes that affect the build system or external dependencies (e.g., `pyproject.toml`, `uv`)      |
| `ci`       | Changes to CI configuration files and scripts (e.g., GitHub Actions workflows)                    |
| `revert`   | Reverts a previous commit                                                                         |
| `chore`    | Routine maintenance, tool configurations, or auxiliary tasks that don't alter source or test code |

#### Scope Naming Rules for Statistical Models

When using `feat` or `fix` related to a statistical model, to avoid overly long `<scope>`, you can refer to the following table and use abbreviations instead:

| Scope Abbreviation | Model Path                              |
| ------------------ | --------------------------------------- |
| `cc`               | `correlation.ci`                        |
| `ci`               | `correlation.inequality`                |
| `msc`              | `mean.single.ci`                        |
| `msi`              | `mean.single.inequality`                |
| `mse`              | `mean.single.equivalence`               |
| `msn`              | `mean.single.noninferiority`            |
| `mss`              | `mean.single.superiority`               |
| `mic`              | `mean.independent.ci`                   |
| `mii`              | `mean.independent.inequality`           |
| `mie`              | `mean.independent.equivalence`          |
| `min`              | `mean.independent.noninferiority`       |
| `mis`              | `mean.independent.superiority`          |
| `psc`              | `proportion.single.ci`                  |
| `psi`              | `proportion.single.inequality`          |
| `pse`              | `proportion.single.equivalence`         |
| `psn`              | `proportion.single.noninferiority`      |
| `pss`              | `proportion.single.superiority`         |
| `pic`              | `proportion.independent.ci`             |
| `pii`              | `proportion.independent.inequality`     |
| `pie`              | `proportion.independent.equivalence`    |
| `pin`              | `proportion.independent.noninferiority` |
| `pis`              | `proportion.independent.superiority`    |

For model names not covered in the table above, you may use the acronym of the name.

## 🚀 Submitting a Pull Request (PR)

1. Create and switch to a topic branch:

   ```bash
   git switch -c feature/your-feature-name
   ```

2. Implement your changes and write unit tests for new functionality or bug fixes.

3. Run local code quality and test checks to ensure everything passes cleanly:

   ```bash
   uv run ruff format
   uv run ruff check
   uv run pytest
   ```

4. Stage and commit your changes following the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) specification:

   ```bash
   git add .
   git commit -m "feat(scope): short description of your changes"
   ```

5. Push your branch to GitHub and open a PR targeting the `main` branch.

   ```bash
   git push -u origin feature/your-feature-name
   ```

Thank you for contributing to PyStatPower! 🚀
