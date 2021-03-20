import numpy as np
import scipy
import scipy as sp
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import stats
import math
import audioop
import binascii
from collections import Counter

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
for x in prob:
    entropy += x * math.log2(1 / x)
print(entropy)