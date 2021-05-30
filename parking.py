import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import random

n = 12000
target_k = 3523
target_o = 21.9
k = 1

x = 0
y = 0

data_2 = open("randomBig.bin", "rb")
data = np.fromfile(data_2, dtype=np.uint32)
data = data.tolist()

print(len(data))
x_array = []
y_array = []
p_values = []

for i in range(0, 1200000):
    y_array.append(random.random() * 100.0)
    #y_array.append(float(data[i])*100.0/256.0)
    # print(y_array)
for i in range(0, 1200000):
    x_array.append(random.random() * 100.0)
    #x_array.append(float(data[i+1200000])*100.0/256.0)
    # print(x_array)
used_cars = 0
successes = list()
counter = []
for test_nr in range(0, 100):
    success_counter = 0
    parkedx = []
    parkedy = []
    for i in range(used_cars, used_cars + 12000):
        crash = False
        x = x_array[i]
        y = y_array[i]

        for j in range(0, len(parkedx)):
            if abs(x - parkedx[j]) <= 1.0 and abs(y - parkedy[j]) <= 1.0:
                crash = True
                # print(i, j, x, y, parkedx[j], parkedy[j])
                break

        if not crash:
            parkedx.append(x)
            parkedy.append(y)
            success_counter += 1

    used_cars += 12000
    success = (success_counter - 3523.0) / 21.9
    successes.append(success)
    p_val = stats.norm.sf(abs(success))  # twosided
    p_values.append(p_val)
    print(test_nr, success_counter)
    counter.append(success_counter)
print(successes)
print(stats.kstest(successes, 'norm'))

print('Srednia liczba udanych parkowan:', np.mean(success_counter))
# Hist1
plt.hist(successes, bins = 20, stacked=True, weights=np.zeros_like(successes) + 1. / len(successes))
plt.title("Rozkład ilości udanych parkowań")
plt.xlabel("Wartość")
plt.ylabel("Częstotliwość występowania")
plt.grid(which='minor')
plt.show()
# Hist2
plt.hist(p_values, bins = 20, stacked=True, weights=np.zeros_like(p_values) + 1. / len(p_values))
plt.title("Rozkład wartosci p")
plt.xlabel("Wartość")
plt.ylabel("Częstotliwość występowania")
plt.grid(which='minor')
plt.show()
