import random


class TSPIndividual:
    id_counter = 0

    def __init__(self, genotype=None):
        self.fitnesses = dict()
        self.id = TSPIndividual.id_counter
        TSPIndividual.id_counter += 1

        if genotype is None:
            self.genotype = self.generate_random_simple_genotype()

        else:
            self.genotype = genotype

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
