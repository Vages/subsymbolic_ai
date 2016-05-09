from collections import defaultdict


class EvolutionWorld:



def fast_non_dominated_sort(population):
    """
    Sorts the population into non-dominated fronts.

    :param population: A population of individuals that have the dominates property.
    :return:
    """
    domination_set = defaultdict(set)
    domination_count = defaultdict(int)
    rank = dict()
    f = [set()]

    for p in population:
        for q in population:
            if q == p:
                continue
            if p.dominates(q):
                domination_set[p].add(q)  # Add q to the set of solutions dominated by p
            elif q.dominates(p):
                domination_count[p] += 1  # Increment the domination counter of p

        if domination_count[p] == 0:  # p belongs to the first front
            rank[p] = 0  # EDIT: Ranks start at 0 instead of 1
            f[0].add(p)

    i = 0  # Initialize the front counter. EDIT: Starts at 0

    while f[i]:  # Set contains elements
        next_front = set()  # Replacement for Q in pseudo code
        for p in f[i]:
            for q in domination_set[p]:
                domination_count[q] -= 1

                if domination_count[q] == 0:  # q belongs to next front
                    rank[q] = i + 1
                    next_front.add(q)

        i += 1
        f.append(next_front)

    return f


def crowding_distance_assignment(population):
    distance = defaultdict(int)

    population_list = list(population)
    population_size = len(population_list)

    objectives = population_list[0].fitnesses.keys()

    for m in objectives:
        population_list.sort(key=lambda x: x.fitnesses[m])
        f_min = population_list[0].fitnesses[m]
        f_max = population_list[population_size - 1].fitnesses[m]
        span = f_max - f_min
        if span == 0:  # The population does not vary in this property
            continue
        population_list[0] = population_list[population_size - 1] = float("inf")

        for i in range(1, population_size - 1):
            current_distance = (population_list[i + 1].fitnesses[m] - population_list[i - 1].fitnesses[m]) / span

            distance[population_list[i]] += current_distance

    return distance


def load_travel_data():
    import pickle
    try:
        with open("traveling_salesman/travel_data/Distance.pickle", "rb") as d_file:
            distances = pickle.load(d_file)
        with open("traveling_salesman/travel_data/Cost.pickle", "rb") as c_file:
            costs = pickle.load(c_file)
    except IOError:
        from openpyxl import load_workbook

        costs = load_workbook('traveling_salesman/travel_data/Cost.xlsx', read_only=True)
        distances = load_workbook('traveling_salesman/travel_data/Distance.xlsx', read_only=True)

        costs = convert_sheet_to_map(costs["Sheet1"])
        distances = convert_sheet_to_map(distances["Sheet1"])

        with open("traveling_salesman/travel_data/Distance.pickle", "wb") as d_file:
            pickle.dump(distances, d_file)

        with open("traveling_salesman/travel_data/Cost.pickle", "wb") as c_file:
            pickle.dump(costs, c_file)

    return costs, distances


def convert_sheet_to_map(sheet):
    costs = dict()
    for row in range(2, sheet.max_row + 1):
        for column in range(2, row + 1):
            data = sheet.cell(row=row, column=column).value

            actual_first_city_number = column - 1
            actual_second_city_number = row - 1
            first_way = (actual_first_city_number, actual_second_city_number)
            second_way = (actual_second_city_number, actual_first_city_number)

            costs[first_way] = data
            costs[second_way] = data

    return costs
