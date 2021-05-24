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

data_2 = open("file.bin", "rb")
data = np.fromfile(data_2, dtype=np.uint32)
data = data.tolist()

x_array = []
y_array = []


for i in range(0, 1200000):
    #y_array.append(random.random()  * 100.0)
    y_array.append(float(data[i])*100.0/256.0)
    #print(y_array)
for i in range(0, 1200000):
    #x_array.append(random.random()  * 100.0)
    x_array.append(float(data[i+1200000])*100.0/256.0)
    #print(x_array)
used_cars = 0
successes = list()
for test_nr in range(0, 100):
    success_counter = 0
    parkedx = []
    parkedy = []
    for i in range(used_cars, used_cars+12000):
        crash = False
        x = x_array[i]
        y = y_array[i]

        for j in range(0, len(parkedx)):
            if abs(x - parkedx[j]) <= 1.0 and abs(y - parkedy[j]) <= 1.0:
                crash = True
                #print(i, j, x, y, parkedx[j], parkedy[j])
                break

        if not crash:
            parkedx.append(x)
            parkedy.append(y)
            success_counter += 1

    used_cars += 12000
    successes.append((success_counter - 3523.0) / 21.9)
    print(test_nr, success_counter)
print(successes)
print(stats.kstest(successes, 'norm'))
