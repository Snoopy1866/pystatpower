# Quickstart

(usage/installation)=

## Installation

To use PyStatPower, first install the [Python](https://www.python.org/downloads/) interpreter, version 3.10+ is supported.

Then, you can install PyStatPower using pip:

```bash
pip install pystatpower
```

To check is the PyStatPower is installed correctly, you can run the following code:

```bash
python -m pystatpower
```

If you see the output similarily as below, the PyStatPower is installed correctly:

```bash
pystatpower version 0.0.2
```

## Examples

PyStatPower provide many modules for power analysis under different scenarios. Here are some examples:

1. **Solve for sample size under one proportion test**

   ```python
   from pystatpower.models import one_proportion

   result = one_proportion.solve_for_sample_size(
       alpha=0.05,
       power=0.80,
       nullproportion=0.80,
       proportion=0.95,
       alternative="two_sided",
       test_type="exact_test"
   )
   print(result)
   ```

   Output:

   ```bash
   42.0
   ```

2. **Solve for sample size under two independent proportion test**

   ```python
   from pystatpower.models import two_proportion

   result = two_proportion.solve_for_sample_size(
       alpha=0.05,
       power=0.80,
       treatment_proportion=0.95,
       reference_proportion=0.80,
       alternative="two_sided",
       test_type="z_test_pooled",
   )
   print(result)
   ```

   Output:

   ```bash
   (76.0, 76.0)
   ```

3. **Solve for power under two independent proportion test**

   ```python
   from pystatpower.models.two_proportion import solve_for_power, GroupAllocation

   result = solve_for_power(
       alpha=0.05,
       treatment_proportion=0.95,
       reference_proportion=0.80,
       alternative="two_sided",
       test_type="z_test_pooled",
       group_allocation=GroupAllocation(
           size_of_treatment=100,
           size_of_reference=50,
       ),
   )
   print(result)
   ```

   Output:

   ```bash
   0.7865318578853373
   ```
