import os
from collections import Counter
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile

number_of_samples = 100000
f_name = "white_noise.wav"
rate, data = wavfile.read(f_name)
bins = 255
print('data lenght:', len(data))
tab = []
c = 0
for x in data:
    if c < number_of_samples:
        if x < 2 ** 14 and x > -(2 ** 14):
            x = x + 2 ** 14
            x = x >> 7
            tab.append(x)
            c += 1
print('f[Hz]:', rate)

plt.hist([tab], bins, range=[0, 255])
plt.show()
print('Max probe:', max(tab))
print('Min probe:', min(tab))
count = Counter(tab)
prob = []
for x in count:
    prob.append(count.get(x) / number_of_samples)

entropy = 0
for x in prob:
    entropy += x * math.log2(1 / x)
print('entropy:', entropy)

#tutaj dzialalem ja i nie dziala pozdro
threshold = 100
watchdog = 0
initial_samples = 1000
temp_prev = [0]
curr_samp = []
runcnt = 0

var = np.var(tab[:initial_samples])
halfvar = var / 2
print('halfvar:', halfvar)






#for i in tab[watchdog:threshold]:
#    for x in temp_prev:
#        x = x << 2
#        curr_samp.append(10 + (int.from_bytes(os.urandom(1), byteorder='big') * i + x) % 25)
#        if ((curr_samp - temp_prev) ** 2) < halfvar:
#            curr_samp.append(10 + temp_prev + ((curr_samp ** watchdog)) % 25)
#print(curr_samp)


if watchdog < threshold:
    for i, curr_samp in enumerate(tab[watchdog:threshold]):
        if i>0:
            curr_samp.append(10 + (int.from_bytes(os.urandom(1), byteorder='big') * i + x) % 25)
            x = curr_samp[i] << 2
            while (curr_samp[i]-curr_samp[i-1])**2 < halfvar:
                curr_samp.append(10+(curr_samp[i-1]+((curr_samp ** watchdog)+runcnt)) % 25)
                watchdog += 1
            else:


