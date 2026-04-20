from pystatpower.models import proportion

size = proportion.independent.noninferiority.solve_size(
    treatment_proportion=0.95,
    reference_proportion=0.90,
    margin=-0.10,
    ratio=1,
    alpha=0.025,
    power=0.8,
)
print(size)
