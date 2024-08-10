import matplotlib.pyplot as plt
import numpy as np
import math

x = np.linspace(-10, 10, 100)
z = 1 / (1 + np.exp(-x))

plt.plot(x, z)
plt.xlabel("x")
plt.ylabel("Sigmoid(X)")

plt.show()

num_plots = short_k.size + 1
plt.figure(figsize=(6 * num_plots, 6), dpi=120)
first_plot = plt.subplot(1, num_plots, 1)
first_plot.set_title("Spectrum (dk=" + str(dk)+")")
im = first_plot.imshow(Z, cmap=plt.cm.RdBu, aspect='auto', extent=[min(k), max(k), min(w), max(w)], origin='lower')  # drawing the function
plt.colorbar(im)