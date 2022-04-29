from server.models import *
from server import db
from routing.ant_colony_optimization import AntColonyOptimizer
import numpy as np

def getBinsToCollect():
    urgentBins = BinData.query.filter(
        (BinData.distance < 15) | (BinData.humidity > 75)
    )
    urgentBinIds = set([x.id for x in urgentBins])

    possibleBins = Bin.query.filter(
        Bin.fill_rate > 60
    )
    possibleBinIds = set([x.id for x in possibleBins])

    binsToCollect = list(possibleBinIds.union(urgentBinIds))
    return binsToCollect

def makeOptimalRoute(bins):
    if len(bins) == 0:
        return None
    problem = np.zeros([len(bins), len(bins)])
    print(problem)
    pToBin = {i: bins[i] for i in range(len(bins))}
    print(pToBin)
    for i in range(len(bins)):
        for j in range(len(bins)):
            x = Distances.query.filter(
                (Distances.bin_one == pToBin[i]) &
                (Distances.bin_two == pToBin[j])
            ).first()
            problem[i][j] = 0 if x is None else x.distance
    print(problem)
    optimizer = AntColonyOptimizer(ants=10, evaporation_rate=.1, intensification=2, alpha=1, beta=1, beta_evaporation_rate=0, choose_best=.1)
    bestPath = optimizer.fit(problem, 100)
    print(bestPath)
    bestPathById = [pToBin[i] for i in bestPath]
    graphById = np.zeros([len(bins), len(bins)])
    print(bestPathById)
    return bestPathById, problem, pToBin
    # return bins