from routing.ant_colony_optimization import AntColonyOptimizer
import numpy as np

problem = np.array([
    [0, 1, 3, 5],
    [1, 0, 2, 5],
    [3, 2, 0, 3],
    [5, 5, 3, 0]
])

optimizer = AntColonyOptimizer(ants=10, evaporation_rate=.1, intensification=2, alpha=1, beta=1, beta_evaporation_rate=0, choose_best=.1)
best = optimizer.fit(problem, 100)
