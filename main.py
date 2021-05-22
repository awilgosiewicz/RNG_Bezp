from collections import Counter
import math
import matplotlib.pyplot as plt
import numpy as np
from scipy import stats
from scipy.io import wavfile
import random


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
    return np.uint8(tab)


def fancyXor(x1, x2, x3):
    result = 0
    for el in x1:
        result = result ^ el
    for el in x2:
        result = result ^ el
    for el in x3:
        result = result ^ el
    return result


def count_entropy(x, amount_of_samples):
    # entropy
    count = Counter(x)
    prob = []
    for x in count:
        prob.append(count.get(x) / amount_of_samples)
    entropy = 0
    for x in prob:
        entropy += x * math.log2(1 / x)
    print('entropy: ', entropy)


def chunk_data(amount_of_samples, data_for_chunking):
    amount_of_chunks = amount_of_samples / 12500
    chunked_array = np.array_split(data_for_chunking, amount_of_chunks)
    print("Number of chunks:", amount_of_chunks)
    return chunked_array


def halfvar_get(halfvar_data):
    initial_samples = 1000
    halfvar_count = stats.iqr(halfvar_data[:initial_samples])
    return halfvar_count


number_of_samples = 100000
f_name = "sound_2.wav"
rate, data = wavfile.read(f_name)
print('data length:', len(data))

samples = sampleGet()
print(chunk_data(number_of_samples, samples))

count_entropy(samples, number_of_samples)
plt.hist(samples, bins=256, range=[0, 255], density=True)
plt.title('Znormalizowany rozkład zmiennych losowych generowanych przez źródło szumu:')
plt.xlabel('Wartosc probki (x)')
plt.ylabel('Czestotliwosc wystepowania (p)')
plt.show()

threshold: int = 100
watchdog: int = 0
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

halfvar = halfvar_get(samples)
print(halfvar)

for i, sample in enumerate(samples):
    SPP = SP
    SP = S
    S = 10 + (sample * i + (SP << 2)) % 256
    watchdog = 0
    while watchdog < threshold:
        if ((S - SP) ** 2) < halfvar:

            S = 10 + (SP + ((S ** watchdog) + runcnt)) % 256
            watchdog += 1
        else:
            Si.append(S)
            watchdog = 100

j = 0
number_of_random_numbers = 1000
while j < number_of_random_numbers:
    random_byte += (1 & fancyXor(Si, SPi, SPPi)) * (2 ** (j % 8))
    SPi.append(Si[j])
    if j % 8 == 7:
        SPPi.append(Si[j])
        random_numbers.append(random_byte % 256)
        random_byte = 0
    else:
        random_numbers.append(random.choice(Si))
    j += 1

print(random_numbers)
count_entropy(random_numbers, number_of_random_numbers)
plt.hist(random_numbers, bins=256, range=[0, 255], density=True)
plt.title('Znormalizowany rozkład zmiennych losowych po post-processingu:')
plt.xlabel('Wartosc probki (x)')
plt.ylabel('Czestotliwosc wystepowania (p)')
plt.show()

DataToSave = np.array(random_numbers)
np.savetxt('file.txt', DataToSave, delimiter='\n', fmt='%f')
