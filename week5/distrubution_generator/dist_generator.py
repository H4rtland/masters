import math
import random

import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson

class Model:
    def __init__(self, p1, p2, p3, p4):
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.p4 = p4

    def model_at(self, x):
        scale = x/14
        a1 = self.p1 * math.pow(1-scale, self.p2)
        a2 = self.p3 + (self.p4 * math.log(scale))
        a3 = math.pow(scale, a2)
        
        return a1*a3

bins = [1.006, 1.037, 1.068, 1.1, 1.133, 1.166, 1.2, 1.234, 1.269, 1.305, 1.341, 1.378, 1.416,
        1.454, 1.493, 1.533, 1.573, 1.614, 1.656, 1.698, 1.741, 1.785, 1.83, 1.875, 1.921, 1.968,
        2.016, 2.065, 2.114, 2.164, 2.215, 2.267, 2.32, 2.374, 2.429, 2.485, 2.542, 2.6, 2.659,
        2.719, 2.78, 2.842, 2.905, 2.969, 3.034, 3.1, 3.167, 3.235, 3.305, 3.376, 3.448, 3.521,
        3.596, 3.672, 3.749, 3.827, 3.907, 3.988, 4.07, 4.154, 4.239, 4.326, 4.414, 4.504, 4.595,
        4.688, 4.782, 4.878, 4.975, 5.074, 5.175, 5.277, 5.381, 5.487, 5.595, 5.705, 5.817, 5.931,
        6.047, 6.165, 6.285, 6.407, 6.531, 6.658, 6.787, 6.918, 7.052, 7.188, 7.326, 7.467, 7.61,
        7.756, 7.904, 8.055, 8.208, 8.364, 8.523, 8.685, 8.85, 9.019, 9.191, 9.366, 9.544, 9.726, 9.911]

bin_widths = [(b-a) for b, a in zip(bins[1:], bins)]



x_range = np.arange(1, 10, 0.1)

model = Model(1.70475e1, 8.43990, -4.63149, -2.43023e-3)



fig, ax = plt.subplots(figsize=(5,4))


ax.loglog(x_range, [model.model_at(x) for x in x_range], color="black", label="Model")

ax.set_xlim(left=1, right=10)
ax.set_ylim(bottom=1, top=1e6)

ax.yaxis.grid(True)
ax.xaxis.grid(True, which="both")


generated_data = [poisson.ppf(random.random(), model.model_at(left)) for left in bins]

ax.scatter(bins, generated_data,
           color="red", marker="x", zorder=20, s=20, label="Generated")

ax.legend()

plt.show()
