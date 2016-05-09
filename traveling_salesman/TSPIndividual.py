import random


class TSPIndividual:
    id_counter = 0

    def __init__(self):
        self.fitnesses = dict()
        pass

    def dominates(self, other):
        pass


def generate_random_simple_genotype(length=48):
    genotype = [i + 1 for i in range(48)]
    random.shuffle(genotype)

    return genotype
