from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile

number_of_samples = 100000
f_name = "white_noise.wav"
rate, data = wavfile.read(f_name)
bins = 255
print(len(data))
tab = []
c = 0
for x in data:
    if c < number_of_samples:
        if x < 2 ** 14 and x > -(2 ** 14):
            x = x + 2 ** 14
            x = x >> 7
            tab.append(x)
            c += 1
print(rate)

plt.hist([tab], bins, range=[0, 255])
plt.show()
print(max(tab))
print(min(tab))
count = Counter(tab)
prob = []
for x in count:
    prob.append(count.get(x) / number_of_samples)

entropy = 0

#tutaj dzialalem ja i nie dziala pozdro
threshold = 100
watchdog = 0
initial_samples = 1000
temp_prev = [0]
curr_samp = []
runcnt = 0

var = np.var(data[:initial_samples])
halfvar = var / 2
print(halfvar)

for i in data[watchdog:threshold]:
    for x in temp_prev:
        x = x << 2
        curr_samp.append(10 + (int.from_bytes(os.urandom(1), byteorder='big') * i + x) % 25)
        if ((curr_samp - temp_prev) ** 2) < halfvar:
            curr_samp.append(10 + temp_prev + ((curr_samp ^ watchdog)) % 25)
print(curr_samp)

