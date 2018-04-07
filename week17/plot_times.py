import os
import os.path as op

import matplotlib
matplotlib.use('PDF')
import matplotlib.pyplot as plt

fig, ax = plt.subplots(6, 2, figsize=(5, 8))

for m in range(2000, 7001, 500):
    limits = []
    times = []
    for file in os.listdir("results/55829/"):
        if file.startswith("times") and file.endswith("{}.txt".format(m)):
            with open(op.join("results/55829/", file), "r") as f:
                for line in f.readlines():
                    l, t = line.split(":")
                    if l == "None":
                        continue
                    l, t = float(l), float(t)
                    limits.append(l)
                    times.append(t)
    #limits = [l/max(limits) for l in limits]
    #ax.scatter(limits, times)
    bins = [x/10 for x in range(0, 55, 1)]
    i = int((m-2000)/500)
    row = int(i%6)
    col = i//6
    n, bins, patches = ax[row][col].hist(times, bins=bins, label="M={}".format(m))
    ax[row][col].set_title("M={}".format(m), fontsize=10)
    #ax[row][col].set_xlabel("time")

#ax.legend()
plt.tight_layout()
plt.savefig("times.pdf")
