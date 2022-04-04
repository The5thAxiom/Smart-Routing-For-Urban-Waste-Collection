import random

from numpy import void

class Ant:
    trailSize = 0
    trail = []
    visited = []

    def __init__(self, tourSize):
        self.trailSize = tourSize
        self.trail = [0 for i in range(tourSize)]
        self.visited = [False for i in range(tourSize)]
    
    def __str__(self) -> str:
        s = f'ant with trailSize: {self.trailSize}\nvisited: {self.visited}\ntrail: {self.trail}'
        return s

    def visitCity(self, currentIndex, city):
        self.trail[currentIndex + 1] = city
        self.visited[city] = True

    def isVisited(self, i):
        return self.visited[i]
    
    def trailLen(self, graph):
        len = graph[self.trail[self.trailSize - 1]][self.trail[0]]
        for i in range(self.trailSize - 1):
            length += graph[self.trail[i]][self.trail[i + 1]]
    
    def clear(self):
        for i in range(self.trailSize):
            self.visited[i] = False


class AntColonyOptimization:
    c = 1.0
    alpha = 1
    beta = 5
    evap = 0.5
    q = 500
    antFactor = 0.8
    randomFactor = 0.01

    maxIterations = 1000

    numberOfCities = 0
    numberOfAnts = 0
    graph = []
    trails = []
    ants = []
    probabilities = []

    currentIndex = 0
    bestTourOrder = []
    bestTourLength = 0

    def __init__(self, numCities): # 7
        self.graph = [
        #    p  r  a  b  u  s  x
            [0, 3, 0, 4, 0, 4, 0], # p
            [3, 0, 1, 0, 0, 0, 0], # r
            [0, 1, 0, 0, 0, 0, 3], # a
            [4, 0, 0, 0, 1, 2, 0], # b
            [0, 0, 0, 1, 0, 0, 3], # u
            [4, 0, 0, 2, 0, 0, 1], # s
            [0, 0, 3, 0, 3, 1, 0]  # x
        ]

        self.numberOfCities = len(self.graph)
        self.numberOfAnts = int(self.numberOfCities * self.antFactor)
        self.trails = [
            [
                0.0 for i in range(self.numberOfCities)
            ] for j in range(self.numberOfCities)
        ]
        self.probabilities = [0.0 for i in range(self.numberOfCities)]
        self.ants = [Ant(self.numberOfCities) for i in range(self.numberOfAnts)]

    def show(self):
        print(self.graph)
        print(self.trails)
        # for ant, i in enumerate(self.ants):
        #     print(i, end = '->')
        #     print(ant)
        print(self.probabilities)

    def startAntOptimization(self):
        for i in range(3):
            print(f"try #{i}")
            self.solve()

    def solve(self):
        self.setupAnts()
        self.clearTrails()
        for i in range(self.maxIterations):
            self.moveAnts()
            self.updateTrails()
            self.updateBest()
        print(f'best tour len: {self.bestTourLength - self.numberOfCities}')
        print(f'best tour order:', end = ' ')
        print(self.bestTourOrder)
        x = [i for i in self.bestTourOrder]
        return x

    def setupAnts(self):
        for i in range(self.numberOfAnts):
            for ant in self.ants:
                ant.clear()
                ant.visitCity(-1, random.randint(0, self.numberOfCities))
        self.currentIndex = 0

    def moveAnts(self):
        for i in range(self.currentIndex, self.numberOfCities - 1):
            for ant in self.ants:
                ant.visitCity(
                    self.currentIndex,
                    self.selectNextCity(ant)
                )
                self.currentIndex += 1

    def selectNextCity(self, ant: Ant) -> int:
        t = random.randint(0, self.numberOfCities - self.currentIndex)
        if random.random() < self.randomFactor:
            cities = filter(
                lambda i: i == t and not ant.isVisited(i),
                range(0, self.numberOfCities)
            )[0]
            if cities != []:
                cityIndex = cities[0]
        self.calculateProbabilites(ant)
        r = random.random()
        total = 0
        for i in range(self.numberOfCities):
            total += self.probabilities[i]
            if total >= r:
                return i


    def calculateProbabilites(self, ant: Ant):
        i = ant.trail[self.currentIndex]
        pheromone = 0.0
        for l in range(self.numberOfCities):
            if not ant.isVisited(1):
                pheromone += self.trails[i][l] ** self.alpha + (1.0/self.graph[i][l]) ** self.beta
        for j in range(self.numberOfCities):
            if ant.isVisited(j):
                self.probabilities[j] = 0.0
            else:
                num = self.trails[i][j] ** self.alpha + (1.0/self.graph[i][j]) ** self.beta
                self.probabilities[j] = num / pheromone

    def updateTrails(self):
        for i in range(self.numberOfCities):
            for j in range(self.numberOfCities):
                self.trail[i][j] *= self.evap
        for a in self.ants:
            contribution = self.q / a.trailLen(self.graph)
            for i in range(self.numberOfCities):
                self.trails[a.trail[i]][a.trail[i + 1]] += contribution
            self.trails[a.trail[self.numberOfCities - 1]][a.trail[0]] += contribution

    def updateBest(self):
        if self.bestTourOrder == []:
            self.bestTourOrder = self.ants[0].trail
            self.bestTourLength = self.ants[0].trailLen(self.graph)
        for a in self.ants:
            if a.trailLen(self.graph) < self.bestTourLength:
                self.bestTourLength = a.trailLen(self.graph)
                self.bestTourOrder = [i for i in a.trail]

    def clearTrails(self):
        for i in range(self.numberOfCities):
            for j in range(self.numberOfCities):
                self.trails[i][j] = self.c

aco = AntColonyOptimization(7)
aco.show()
aco.startAntOptimization()