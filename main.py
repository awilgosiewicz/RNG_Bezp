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

def sampleGet():
    c=0
    tab=[]
    for x in data:
        if c < number_of_samples:
            if x < 2 ** 14 and x > -(2 ** 14):
                x = x + 2 ** 14
                x = x >> 7
                tab.append(x)
                c += 1
    return tab


plt.hist([sampleGet()], bins, range=[0, 255])
plt.show()
print('Max probe:', max(sampleGet()))
print('Min probe:', min(sampleGet()))
count = Counter(sampleGet())
prob = []
for x in count:
    prob.append(count.get(x) / number_of_samples)

entropy = 0
for x in prob:
    entropy += x * math.log2(1 / x)
print('entropy:', entropy)


threshold: int = 100
watchdog: int = 0
initial_samples = 1000
temp_prev = [0]
curr_samp = []
random_bit = [0]
runcnt = 0
sample = 0
previous =0

var = np.var(sampleGet()[:initial_samples])
halfvar = var / 2
print('halfvar:', halfvar)


if watchdog < threshold:
    for i, sample in enumerate(sampleGet()[watchdog:threshold]):
            curr_samp.append(10 + (int.from_bytes(os.urandom(1), byteorder='big') * i + previous) % 25)
            previous = curr_samp[i] << 2
            while ((curr_samp[i] - curr_samp[i-1]) ** 2) < halfvar:
                curr_samp.append(10 + (curr_samp[i - 1] + ((curr_samp[i] ** watchdog) + runcnt)) % 25)
                watchdog += 1
                # TODO przesuwanie tablicy żeby pobrać inne sample
            else:
                print('dupa')
                # TODO random_bit[i]
                for x, random in enumerate(random_bit[0:7]):
                    random = 1 & (curr_samp[i] ^ curr_samp[i-1] ^ curr_samp[i-2] )
                    x += 1
