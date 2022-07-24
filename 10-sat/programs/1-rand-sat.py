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
    a, b, c, d, e, f = generate_random_values(6)

    satisfied += count_satisfied_clauses([a, not b, not c], [not a, d, e], [e, f])

average = satisfied / experiments
print(f"{average:.2f}/3 ~= {average/3:.2f}%")
