"""
Simple demo of a scatter plot.
"""
import json

import numpy as np
import os
import matplotlib.pyplot as plt

log_location = "logs"

log_files = list(os.walk(log_location))[0][2]

default_file = log_files[-1]

with open(os.path.join(log_location, default_file), 'r') as log_contents:
    log_data = json.load(log_contents)

plot_counter = 121

def draw_plot(front_list=log_data, plot_title="All fronts"):
    global plot_counter
    x, y = [], []
    largest_cost = -float("inf")
    largest_cost_data = ()
    smallest_cost = float("inf")
    smallest_cost_data = ()
    largest_distance = -float("inf")
    largest_distance_data = ()
    smallest_distance = float("inf")
    smallest_distance_data = ()
    for front in front_list:
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

    # area = np.pi * (15 * np.random.rand(N))**2  # 0 to 15 point radiuses
    plt.subplot(plot_counter)
    plot_counter += 1
    plt.scatter(x, y, alpha=0.5)
    plt.xlabel("distance")
    plt.ylabel("cost")
    plt.title(plot_title)
    plt.text(smallest_distance_data[0], smallest_distance_data[1],
             "(" + str(smallest_distance_data[0]) + ", " + str(smallest_distance_data[1]) + ")")
    plt.text(largest_distance_data[0], largest_distance_data[1],
             "(" + str(largest_distance_data[0]) + ", " + str(largest_distance_data[1]) + ")")
    plt.text(smallest_cost_data[0], smallest_cost_data[1],
             "(" + str(smallest_cost_data[0]) + ", " + str(smallest_cost_data[1]) + ")")
    plt.text(largest_cost_data[0], largest_cost_data[1],
             "(" + str(largest_cost_data[0]) + ", " + str(largest_cost_data[1]) + ")")
    plt.grid(True)

draw_plot()
draw_plot(front_list=[log_data[0]], plot_title="Pareto front")
plt.show()
