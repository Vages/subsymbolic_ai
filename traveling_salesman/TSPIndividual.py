import random


class MOOPIndividual:
    def __init__(self):
        self.fitnesses = dict()

    def dominates(self, other):
        """
        Returns whether this object dominates the other. Assumes that the goal is to minimize all objectives.

        A solution is said to dominate another if it is no worse than the other in all objectives and superior
        in at least one. (Lecture slides 9, p. 23)

        :param other: Another TSPIndividual
        :return:
        """
        dominates_in_one_objective = False
        for k in self.fitnesses:
            self_score = self.fitnesses[k]
            other_score = other.fitnesses[k]

            if self_score < other_score:
                dominates_in_one_objective = True
            if self_score > other_score:
                return False

        return dominates_in_one_objective

    def __str__(self):
        return str(self.fitnesses)

    def __repr__(self):
        return self.__str__()


class TSPIndividual(MOOPIndividual):
    id_counter = 0

    def __init__(self, cost_dict, genotype=None):
        super(TSPIndividual, self).__init__()
        self.id = TSPIndividual.id_counter
        self.cost_dict = cost_dict
        TSPIndividual.id_counter += 1

        if genotype is None:
            self.genotype = self.generate_random_genotype()

        else:
            self.genotype = genotype

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    @staticmethod
    def generate_random_genotype(length=48):
        genotype = [i + 1 for i in range(length)]
        random.shuffle(genotype)

        return genotype

    def get_mutated_genotype(self):
        """
        Returns a copy of the genotype in which two cities have changed places.

        :return: The mutated genotype.
        """
        copied_genotype = self.genotype[:]
        i, j = random.randrange(len(self.genotype)), random.randrange(len(self.genotype))
        copied_genotype[i], copied_genotype[j] = copied_genotype[j], copied_genotype[i]

        return copied_genotype

    def assess_fitness(self):
        """
        Assesses the cost of a complete tour for both dimensions and stores them in the fitness dictionary.
        """
        if not self.fitnesses:  # Fitnesses have not yet been assessed
            for key in self.cost_dict:  # For all the objectives that are to be assessed
                current_costs = self.cost_dict[key]  # The costs for currently examined objective
                counter = 0
                for i in range(len(self.genotype)):
                    first_city, second_city = self.genotype[i - 1], self.genotype[i]
                    counter += current_costs[(first_city, second_city)]  # Add cost of this objective to the counter

                self.fitnesses[key] = counter  # Set the fitness of this objective to what has been counted

    def _convert_genotype_to_edge_dict(self):
        """
        Converts the genotype to a dictionary of the form {city:set(neighbor1, neighbor2)}

        :return: The edge dictionary
        """
        edges = dict()
        for i in range(len(self.genotype)):
            previous_city = self.genotype[i - 1]
            current_city = self.genotype[i]
            next_city = self.genotype[(i + 1) % len(self.genotype)]  # Modulo to avoid index error

            edges[current_city] = {previous_city, next_city}

        return edges

    def mate_with(self, other):
        """
        Uses edge recombination to mate two individuals: https://en.wikipedia.org/wiki/Edge_recombination_operator#cite_note-2

        :param other: Another TSPInvidiual
        :return: Offspring genotype
        """
        my_edge_dict = self._convert_genotype_to_edge_dict()
        other_edge_dict = other._convert_genotype_to_edge_dict()
        combined_edge_dict = dict()

        for city in my_edge_dict:
            combined_edge_dict[city] = my_edge_dict[city].union(other_edge_dict[city])

        my_starting_city = self.genotype[0]
        other_starting_city = other.genotype[0]

        random_starting_city = random.choice([my_starting_city, other_starting_city])

        new_tour = []
        current_city = random_starting_city

        while len(new_tour) < len(self.genotype):
            new_tour.append(current_city)

            connected_cities = combined_edge_dict[current_city]
            del combined_edge_dict[current_city]
            # Delete this city from all its connected cities
            for neighbor_city in connected_cities:
                combined_edge_dict[neighbor_city].remove(current_city)

            if connected_cities:
                # Find the cities with the fewest connections
                fewest_connections = float("inf")
                least_connected_cities = []

                for neighbor_city in connected_cities:
                    connections = len(combined_edge_dict[neighbor_city])
                    if connections == fewest_connections:
                        least_connected_cities.append(neighbor_city)
                    elif connections < fewest_connections:
                        least_connected_cities = [neighbor_city]
                        fewest_connections = connections

                current_city = random.choice(least_connected_cities)

            else:
                remaining_cities = list(combined_edge_dict.keys())
                if remaining_cities:
                    current_city = random.choice(remaining_cities)

        return new_tour
