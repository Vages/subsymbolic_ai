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

x, y = [], []

for front in log_data:
    for item in front:
        dist, cost = item["distance"], item["cost"]
        x.append(dist)
        y.append(cost)

#area = np.pi * (15 * np.random.rand(N))**2  # 0 to 15 point radiuses

plt.scatter(x, y, alpha=0.5)
plt.show()
