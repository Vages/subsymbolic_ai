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

    def test_crowded_comparison_sort(self):
        nodes = [1, 2, 3, 4, 5, 6, 7]
        ranks = {1: 0, 2: 0, 3: 0, 4: 0, 5: 1, 6: 1, 7: 1}
        inf = float("inf")
        distances = {1: inf, 2: 1, 3: 2, 4: inf, 5: inf, 6: 1, 7: inf}

        expected_sequence = [1, 4, 3, 2, 5, 7, 6]

        actual_sequence = EvolutionWorld.crowded_comparison_sort(nodes, ranks, distances)

        self.assertEqual(expected_sequence, actual_sequence)
