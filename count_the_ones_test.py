import collections
from collections import Counter
import numpy as np
import pylab
import scipy.stats as stats
import random
import math
import matplotlib.pyplot as plt
import seaborn as sns

LETTERS_PROB = [37 / 256, 56 / 256, 70 / 256, 56 / 256, 37 / 256]
LETTERS = {'A': 0, 'B': 1, 'C': 2, 'D': 3, 'E': 4}
LETTERS_R = {1: 'A', 2: 'B', 3: 'C', 4: 'D', 5: 'E'}
MEAN = 2500
STANDARD = math.sqrt(5000)
NO_TESTS = 10

def phi(x):
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0


def count_the_ones(byte):
    counter = 0
    while byte:
        counter += byte & 1
        byte = byte >> 1
    return counter


def def_letter(x):
    switcher = {
        0: "A",
        1: "A",
        2: "A",
        3: "B",
        4: "C",
        5: "D",
        6: "E",
        7: "E",
        8: "E"
    }
    return switcher.get(x)


data_2 = open("randomBig.bin", "rb")
data = np.fromfile(data_2, dtype=np.uint32)
p_values = []
chi_sqs = []

for test in range(NO_TESTS):
    array = []
    words4 = []
    words5 = []
    for number in range(256004):
        #array.append(int(data[1+number+test*256004]))
        array.append(int(random.random() * 255.0))
    i = 0
    while i < len(array) - 4:
        # the number of ones
        letters = [
            count_the_ones(array[i]),
            count_the_ones(array[i + 1]),
            count_the_ones(array[i + 2]),
            count_the_ones(array[i + 3]),
            count_the_ones(array[i + 4])
        ]
        letters[0] = def_letter(letters[0])
        letters[1] = def_letter(letters[1])
        letters[2] = def_letter(letters[2])
        letters[3] = def_letter(letters[3])
        letters[4] = def_letter(letters[4])

        words5.append(str(letters[0]) + str(letters[1]) + str(letters[2]) + str(letters[3]) + str(letters[4]))

        i = i + 1

    i = 0
    while i < len(array) - 4:
        # the number of ones
        letters = [
            count_the_ones(array[i]),
            count_the_ones(array[i + 1]),
            count_the_ones(array[i + 2]),
            count_the_ones(array[i + 3])
        ]
        letters[0] = def_letter(letters[0])
        letters[1] = def_letter(letters[1])
        letters[2] = def_letter(letters[2])
        letters[3] = def_letter(letters[3])

        words4.append(str(letters[0]) + str(letters[1]) + str(letters[2]) + str(letters[3]))

        i = i + 1

    # print(words5)
    # print(words4)

    # expected probability of 4 letter words
    exp_prob4 = [0] * 625
    for word in range(625):
        test_word = word
        freq = 256000
        for letter in range(4):
            freq *= LETTERS_PROB[test_word % 5]
            test_word = math.floor(test_word / 5)
        exp_prob4[word] = freq

    # expected probability of 5 letter words
    exp_prob5 = [0] * 3125
    for word in range(3125):
        temp_word = word
        freq = 256000
        for letter in range(5):
            freq *= LETTERS_PROB[temp_word % 5]
            temp_word = math.floor(temp_word / 5)
        exp_prob5[word] = freq

    sorted4 = Counter(words4)
    prob4 = [0] * 625
    i = 0
    for key in sorted(sorted4):
        prob4[i] = sorted4[key]
        i += 1
    # print(prob4)

    sorted5 = Counter(words5)
    prob5 = [0] * 3125
    i = 0
    for key in sorted(sorted5):
        prob5[i] = sorted5[key]
        i += 1
    # print(prob5)

    q4 = 0
    for i in range(625):
        q4 += ((prob4[i] - exp_prob4[i]) ** 2) / exp_prob4[i]
    # print(q4)

    q5 = 0
    for i in range(3125):
        q5 += ((prob5[i] - exp_prob5[i]) ** 2) / exp_prob5[i]
    # print(q5)

    chi_sq = q5 - q4
    #print(chi_sq)
    z = (chi_sq - MEAN) / STANDARD

    #print(z)
    p = 1.0 - phi(z)
    p_values.append(p)
    chi_sqs.append(chi_sq)

print(chi_sqs)
print(p_values)

stat, p_val_ks = stats.kstest(p_values, 'uniform')
print(f"With {NO_TESTS} tests: ")
if 0.025 < p_val_ks < 0.975:
    print(f"Test PASSED with p = {p_val_ks}")
else:
    print(f"Test FAILED with p = {p_val_ks}")

#pvalues histogram
x_axis = np.linspace(0, len(p_values) - 1, num=len(p_values))
plt.hist(p_values, bins = len(p_values) //2, weights=np.zeros_like(p_values) + 1. / len(p_values))
plt.title("Empiryczny rozkład wartości p")
plt.xlabel("Wartość")
plt.ylabel("Częstotliwość występowania")
plt.show()

#expected words[4]
def FreqDistribution(freqs, EXPECTED, word_len):
    sum_freq = sum(freqs)
    sum_expected = sum(EXPECTED)
    x_axis = np.linspace(0, len(freqs) - 1, num=len(freqs))
    y_axis = [freqs[i] / sum_freq for i in range(len(freqs))]

    if word_len == 4:
        start = 0
        end = 625
    elif word_len == 5:
        start = 0
        end = 3125

    y_axis_exp = [EXPECTED[i] / sum_expected for i in range(len(EXPECTED))]
    plt.plot(x_axis, y_axis_exp, 'red', label="Rozkład oczekiwany", alpha = 0.5)
    plt.plot(x_axis, y_axis, label='Rozkład rzeczywisty')
    plt.title("Rozklad dla slow "+str(word_len)+'-literowych')
    plt.xlabel("Wartosc")
    plt.ylabel("Częstotliwość występowania")
    plt.legend(loc="upper right")
    plt.show()

def makeCDF(x, plot=True, *args, **kwargs):
    x, y = sorted(x), np.arange(len(x)) / len(x)
    ideal_x = [0.5] * len(x)
    ideal_y = np.arange(len(ideal_x)) / len(ideal_x)
    plt.title("Empiryczny CDF p")
    plt.xlabel("Wartość p")
    plt.ylabel("Częstotliwość występowania")
    plt.plot(x, y, *args, **kwargs) if plot else (x, y)
    plt.plot(ideal_x, ideal_y, 'orange') if plot else (ideal_x, ideal_y)
    plt.show()


FreqDistribution(prob4, exp_prob4, 4)
FreqDistribution(prob5, exp_prob5, 5)

def cdf(data):

    data_size=len(data)

    # Set bins edges
    data_set=sorted(set(data))
    bins=np.append(data_set, data_set[-1]+1)

    # Use the histogram function to bin the data
    counts, bin_edges = np.histogram(data, bins=bins, density=False)

    counts=counts.astype(float)/data_size

    # Find the cdf
    cdf = np.cumsum(counts)

    # Plot the cdf
    plt.plot(bin_edges[0:-1], cdf,linestyle='--', marker="o", color='b')
    plt.ylim((0,1))
    plt.ylabel("CDF")
    plt.grid(True)

    plt.show()

cdf(p_values)