import json
import os
import matplotlib.pyplot as plt

log_location = "logs"


def draw_plot(front_list, plot_title):
    markers = "o", "s", "^"
    colors = "red", "blue", "yellow"
    x, y = [], []
    largest_cost = -float("inf")
    largest_cost_data = ()
    smallest_cost = float("inf")
    smallest_cost_data = ()
    largest_distance = -float("inf")
    largest_distance_data = ()
    smallest_distance = float("inf")
    smallest_distance_data = ()
    for i, front in enumerate(front_list):
        for item in front:
            dist, cost = item["distance"], item["cost"]
            coordinate = (dist, cost)

            if cost < smallest_cost:
                smallest_cost = cost
                smallest_cost_data = coordinate
            if cost > largest_cost:
                largest_cost = cost
                largest_cost_data = coordinate

            if dist < smallest_distance:
                smallest_distance = dist
                smallest_distance_data = coordinate
            if dist > largest_distance:
                largest_distance = dist
                largest_distance_data = coordinate

            x.append(dist)
            y.append(cost)

        plt.scatter(x, y, marker=markers[i], c=colors[i], alpha=1, s=40)
        x, y = [], []

    # area = np.pi * (15 * np.random.rand(N))**2  # 0 to 15 point radiuses
    plt.xlabel("distance")
    plt.ylabel("cost")
    plt.title(plot_title)
    """
    plt.text(smallest_distance_data[0], smallest_distance_data[1],
             "(" + str(smallest_distance_data[0]) + ", " + str(smallest_distance_data[1]) + ")")
    plt.text(largest_distance_data[0], largest_distance_data[1],
             "(" + str(largest_distance_data[0]) + ", " + str(largest_distance_data[1]) + ")")
    plt.text(smallest_cost_data[0], smallest_cost_data[1],
             "(" + str(smallest_cost_data[0]) + ", " + str(smallest_cost_data[1]) + ")")
    plt.text(largest_cost_data[0], largest_cost_data[1],
             "(" + str(largest_cost_data[0]) + ", " + str(largest_cost_data[1]) + ")")
    """

if __name__ == "__main__":
    logs_to_be_visualized = ["2016-05-11-17:44:46-P100-G8000-M0.5-C0.5-E0.1.log",
                             "2016-05-11-22:07:40-P50-G32000-M0.3-C0.5-E0.1.log",
                             "2016-05-11-21:43:31-P50-G32000-M0.5-C0.5-E0.1.log"]

    pareto_fronts = []

    for file in logs_to_be_visualized:
        with open(os.path.join(log_location, file), 'r') as log_contents:
            first_front = json.load(log_contents)[0]
            pareto_fronts.append(first_front)

    draw_plot(pareto_fronts, "")
    plt.show()
