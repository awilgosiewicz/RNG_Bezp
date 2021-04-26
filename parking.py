import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
n = 12000
target_k = 3523
target_o = 21.9
k = 1

x = 0
y = 0
crash = False
crash_counter = 0


data = open("file.txt", "r")

x_array = []
y_array = []
counter = 0
for i in data:

    if counter % 2:
        y_array.append(round(int(i)/256*100))
    else:
        x_array.append(round(int(i)/256*100))
    counter += 1

print(len(x_array))
print(len(y_array))

for i in range(0, 12000-1):
    x = x_array[i]
    y = y_array[i]
    for j in range(0, i-1):
        if x == x_array[j] and y == y_array[j]:
            crash = True
            crash_counter += 1
            print("Samochod probowal zaparkować na miejscu (", x, ", ", y, ") jednak bylo ono juz zajete i jest to ", i, " samochod")
            break

print(crash_counter)

both_arrays = np.column_stack((x_array, y_array))
plt.figure()
plt.plot(both_arrays, 'r.')
plt.show()

print(both_arrays.shape)
sorted_arrays = np.sort(both_arrays, axis = 0)
scaled_arrays = (sorted_arrays - sorted_arrays.mean())/sorted_arrays.std()

scaled_arrays = np.reshape(scaled_arrays, (24000, ))

normal_numbers = np.random.normal(loc = 0, scale = 1, size = np.size(scaled_arrays))
normal_numbers = np.sort(normal_numbers)

plt.figure()
plt.hist([scaled_arrays, normal_numbers], label = ['crash counter', 'normal'])
plt.xlabel('bins')
plt.ylabel('counts')
plt.legend(loc='best')
ax = plt.gca()
ax.set_facecolor ('#ffffff')
ax.grid(False)
plt.show()


print(stats.kstest(scaled_arrays, 'norm'))
print(stats.ks_2samp(scaled_arrays, normal_numbers))
data.close()