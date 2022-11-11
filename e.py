import random
import matplotlib.pyplot as plt
import numpy as np

x = {}

for i in range(100000):
    num = 0
    for j in range(10):
        if .300 >= random.random():
            num += 1
    if (num / 10) not in x:
        x[num/10] = 1
    else:
        x[num/10] += 1

x = dict(sorted(x.items()))
plt.scatter(np.array(list(x.keys())), np.array(list(x.values())))
plt.plot(np.array(list(x.keys())), np.array(list(x.values())))

print(x, list(zip(x.items())))
plt.show()
