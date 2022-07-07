from mcximings_HungarianAlgorithm import HungarianAlgorithm


cost_matrix = [
    [12, 72, 52, 20, 54],
    [20, 93, 63, 32, 84],
    [83, 43, 61, 12, 44],
    [19, 81, 91, 71, 69],
    [26, 35, 65, 93, 83]
]

a = HungarianAlgorithm()
distribution = a.Solve(cost_matrix)
print(f'{distribution=}')
print(f'{a.cost=}')

for d in distribution:
    print(type(d))
