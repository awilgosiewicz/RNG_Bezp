import random
import math
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt


def FreqDistribution(freqs):
    sum_freq = sum(freqs)
    sum_expected = sum(EXPECTED)
    x_axis = np.linspace(6, len(freqs) - 1 + 6, num=len(freqs))
    y_axis = [freqs[i] / sum_freq for i in range(len(freqs))]
    plt.bar(x_axis, y_axis)
    y_axis = [EXPECTED[i] / sum_expected for i in range(len(EXPECTED))]
    plt.plot(x_axis, y_axis, 'red', label="Rozkład normalny")
    plt.title("Empiryczny rozkład ilości iteracji")
    plt.ylabel("Częstotliwość występowania")
    plt.legend(loc="upper right")
    plt.show()

def Histogram_pval(pval):
    x_axis = np.linspace(0, len(pval) - 1, num=len(pval))
    plt.hist(pval, bins=len(pval)//2, weights=np.zeros_like(pval) + 1. / len(pval))
    plt.title("Empiryczny rozkład wartości p")
    plt.xlabel("Wartość")
    plt.ylabel("Częstotliwość występowania")
    plt.show()

EXPECTED = [2.103, 5.779, 17.554, 46.732, 110.783,
            236.784, 460.944, 824.116, 1362.781, 2096.849,
            3017.612, 4080.197, 5204.203, 6283.828, 7205.637,
            7869.451, 8206.755, 8191.935, 7844.008, 7219.412,
            6398.679, 5470.931, 4519.852, 3613.661, 2800.028,
            2105.567, 1538.652, 1094.02, 757.796, 511.956,
            337.726, 217.787, 137.439, 84.97, 51.518,
            30.666, 17.939, 10.324, 5.851, 3.269,
            1.803, 0.982, 1.121]

NO_TESTS = 20

p_vals = []
chi_sqs = []
random_numbers = []

data = open("randomBig.bin", "rb")
data_array = np.fromfile(data, dtype=np.uint32)
# print(len(data_array))

for number in range(len(data_array)):
    # print(data_array[number])
    #random_numbers.append(data_array[number] / 256.0)
    random_numbers.append(random.random())
print(random_numbers)
random_number_i = 0
for test in range(NO_TESTS):

    j_freqs = [0] * 43
    for test_number in range(100000):
        random_number_i = test * 20 + test_number * 40
        k = 2147483648
        j = 0
        while k != 1 and j <= 48:
            k = math.ceil(k * random.random())
            random_number_i += 1
            j += 1
        if 6 <= j <= 48:
            j_freqs[j - 6] += 1
        elif j < 6:
            j_freqs[0] += 1
        else:
            j_freqs[42] += 1

    # print(j_freqs)

    # chi_sq = 0
    # for i in range(len(j_freqs)):
    #    chi_sq += ((j_freqs[i] - EXPECTED[i]) ** 2) / EXPECTED[i]
    chi_sq, p_val = stats.chisquare(f_obs=j_freqs, f_exp=EXPECTED)

    p_vals.append(p_val)
    chi_sqs.append(chi_sq)
print(j_freqs)
print(EXPECTED)
per_count = 0
for i in range(len(p_vals)):
    if 0.025 < p_vals[i] < 0.975:
        print("test number: " + str(i) + ", p-value = " + str(p_vals[i]) + ", PASSED")
        per_count += 1
    else:
        print("test number: " + str(i) + ", p-value = " + str(p_vals[i]) + ", FAILED")
print("Passed " + str(per_count) + " out of " + str(NO_TESTS) + " (" + str(per_count / NO_TESTS * 100) + "%) tests")
# result = stats.kstest(p_vals, 'uniform')

# print(result)
FreqDistribution(j_freqs)
Histogram_pval(p_vals)

#result = stats.kstest(p_vals, 'uniform')

#Wprint(result)