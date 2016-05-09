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


class TSPIndividual(MOOPIndividual):
    id_counter = 0

    def __init__(self, cost_dict, genotype=None):
        super(TSPIndividual, self).__init__()
        self.id = TSPIndividual.id_counter
        self.cost_dict = cost_dict
        TSPIndividual.id_counter += 1

        if genotype is None:
            self.genotype = self.generate_random_simple_genotype()

        else:
            self.genotype = genotype

    def get_mutated_simple_genotype(self):
        copied_genotype = self.genotype[:]
        i, j = random.randrange(len(self.genotype)), random.randrange(len(self.genotype))
        copied_genotype[i], copied_genotype[j] = copied_genotype[j], copied_genotype[i]

        return copied_genotype

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == other.id

    @staticmethod
    def generate_random_simple_genotype(length=48):
        genotype = [i + 1 for i in range(length)]
        random.shuffle(genotype)

        return genotype

    def assess_fitness(self):
        if not self.fitnesses:  # Fitnesses have not yet been assessed
            for key in self.cost_dict:  # For all the objectives that are to be assessed
                current_costs = self.cost_dict[key]  # The costs for currently examined objective
                counter = 0
                for i in range(len(self.genotype)):
                    first_city, second_city = self.genotype[i - 1], self.genotype[i]
                    counter += current_costs[(first_city, second_city)]  # Add cost of this objective to the counter

                self.fitnesses[key] = counter  # Set the fitness of this objective to what has been counted

    def convert_genotype_to_edge_dict(self):
        edges = dict()
        for i in range(len(self.genotype)):
            previous_city = self.genotype[i-1]
            current_city = self.genotype[i]
            next_city = self.genotype[(i + 1) % len(self.genotype)]  # Modulo to avoid index error

            edges[current_city] = {previous_city, next_city}

        return edges
