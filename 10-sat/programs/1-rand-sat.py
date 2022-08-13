from random import choice


def generate_random_values(n):
    """Return a random assignment of n values."""
    return [choice([True, False]) for _ in range(n)]


def count_satisfied_clauses(*clauses):
    """Count the number of satisfied clauses."""
    total = 0
    for clause in clauses:
        if any(clause):
            total += 1
    return total


experiments = 10000
satisfied = 0

for i in range(experiments):
    a, b, c = generate_random_values(3)

    satisfied += count_satisfied_clauses(
        [a],
        [not a],
        [b, not c],
        [c]
    )

average = satisfied / experiments
print(f"{average:.2f}/4 ~= {average/4:.2f}")
