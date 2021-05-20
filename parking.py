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

data_2 = open("fortnite.bin", "rb")
data = np.fromfile(data_2, dtype=np.uint32)

x_array = []
y_array = []

for i in range(0, 1200000):
    y_array.append(random.random()  * 100.0)
        #y_array.append(round(np.uint32(i)/256*100))
for i in range(0, 1200000):
    x_array.append(random.random()  * 100.0)
        #x_array.append(round(np.uint32(i)/256*100))

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

#plt.figure()
#plt.plot(x_array, y_array, 'r.')
#plt.show()
#
#both_arrays = np.column_stack((x_array, y_array))
#
#print(both_arrays.shape)
#sorted_arrays = np.sort(both_arrays, axis = 0)
#scaled_arrays = (sorted_arrays - sorted_arrays.mean()) / sorted_arrays.std()
#
#scaled_arrays = np.reshape(scaled_arrays, (24000, ))
#
#normal_numbers = np.random.normal(loc = 0, scale = 1, size = np.size(scaled_arrays))
#normal_numbers = np.sort(normal_numbers)
#
#plt.figure()
#plt.hist([scaled_arrays, normal_numbers], label = ['crash counter', 'normal'])
#plt.xlabel('bins')
#plt.ylabel('counts')
#plt.legend(loc='best')
#ax = plt.gca()
#ax.set_facecolor ('#ffffff')
#ax.grid(False)
#plt.show()

#z = success_counter - 3523.0 / 21.9
#print(stats.kstest(z, 'norm'))
#print(stats.ks_2samp(scaled_arrays, normal_numbers))





