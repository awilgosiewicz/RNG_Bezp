from collections import Counter
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy.io import wavfile


def sampleGet():
    c = 0
    tab = []
    for x in data:
        if c < number_of_samples:
            if 2 ** 14 > x > -(2 ** 14):
                x = x + 2 ** 14
                x = x >> 7
                tab.append(x)
                c += 1
    return tab


def fancyxor(x1, x2, x3):
    result = 0
    for el in x1:
        result = result ^ el
    for el in x2:
        result = result ^ el
    for el in x3:
        result = result ^ el
    return result


def hist_and_entropy(x, amount_of_samples):
    #entropy
    count = Counter(x)
    prob = []
    for x in count:
        prob.append(count.get(x) / amount_of_samples)
    entropy = 0
    for x in prob:
        entropy += x * math.log2(1 / x)
    print('entropy: ', entropy)
    #hist
    plt.hist(x, bins = 256, range=[0, 255])
    plt.show()


number_of_samples = 100000
f_name = "white_noise_final.wav"
rate, data = wavfile.read(f_name)
print('data length:', len(data))


samples = sampleGet()
hist_and_entropy(samples, number_of_samples)

threshold: int = 100
watchdog: int = 0
initial_samples = 1000
Si = []
SPi = []
SPPi = []
runcnt = 0
sample = 0
previous = 0
S = 0
SP = 0
SPP = 0
random_byte = 0
random_numbers = []

var = np.var(sampleGet()[:initial_samples])
halfvar = (var / 2) % 25
print('halfvar:', halfvar)


for i, sample in enumerate(samples):
    SPP = SP
    SP = S
    S = 10 + (sample * i + (SP << 2)) % 25
    watchdog = 0
    while watchdog < threshold:
        if ((S - SP) ** 2) < halfvar:

            S = 10 + (SP + ((S ** watchdog) + runcnt)) % 25
            watchdog += 1
        else:
            Si.append(S)
            watchdog = 100

j = 0
number_of_random_numbers = 10000
while j < number_of_random_numbers * 8:
    random_byte += (1 & fancyxor(Si, SPi, SPPi)) * (2 ** (j % 8))
    SPi.append(Si[j])
    if j % 8 == 7:
        SPPi.append(Si[j])
        random_numbers.append(random_byte)
        random_byte = 0
    j += 1

print(random_numbers)
hist_and_entropy(random_numbers, number_of_random_numbers)