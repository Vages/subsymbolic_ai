from unittest import TestCase

from traveling_salesman.MOOPEvolution import EvolutionWorld
from traveling_salesman.TSPIndividual import TSPIndividual


class TestEvolutionWorld(TestCase):
    def test_crowding_distance_assignment(self):
        points = [(1, 4), (2, 3), (4, 1), (5, 0.5)]
        population = set()

        for x, y in points:
            ind = TSPIndividual()
            ind.fitnesses["x"] = x
            ind.fitnesses["y"] = y
            population.add(ind)

        expected_distances = {(1, 4): float("inf"), (5, 0.5): float("inf")}

        x_max = max(points, key=lambda x: x[0])[0]
        x_min = min(points, key=lambda x: x[0])[0]
        y_max = max(points, key=lambda x: x[1])[1]
        y_min = min(points, key=lambda x: x[1])[1]

        expected_distances[(2, 3)] = (4 - 1) / (x_max - x_min) + (4 - 1) / (y_max - y_min)
        expected_distances[(4, 1)] = (5 - 2) / (x_max - x_min) + (3 - 0.5) / (y_max - y_min)

        calculated_distances = EvolutionWorld.crowding_distance_assignment(population)

        for ind in population:
            cartesian = (ind.fitnesses["x"], ind.fitnesses["y"])
            self.assertAlmostEqual(expected_distances[cartesian], calculated_distances[ind], delta=0.001)
