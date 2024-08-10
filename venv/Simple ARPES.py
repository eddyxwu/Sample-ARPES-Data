import matplotlib.pyplot as plt
import numpy as np
import math
import matlab

res = 70

array_1 = np.zeros(res)
array_2 = np.zeros(res)
for i in range(res):
    array_1[i] = i
    array_2[i] = i

print(array_1)
print(array_2)
X, Y = np.meshgrid(array_1, array_2)
print(X)
print(Y)

# variables
a = 8
b = 20
c = 8
p = 8
q = 50
r = 8

# constants
e = 2.71828

def function(x, y):
    return 20*(a * e ** ((-1 * ((x - b) ** 2)) / (2 * (c ** 2))) + (p * e ** ((-1 * ((x - q) ** 2)) / (2 * (r ** 2)))))

Z = function(X, Y)
print(Z)


noise = np.random.poisson(Z, Z.shape)
J = Z + noise
print(J)

im = plt.imshow(J, cmap=plt.cm.RdBu, aspect='auto', extent=[min(array_1), max(array_1), min(array_2), max(array_2)], origin='lower')

plt.colorbar(im)

plt.xlabel("x")
plt.ylabel("y")

plt.show()

