import random
import math
import scipy.stats as stats
import numpy as np

data_2 = open("file.bin", "rb") #rb musi być niby
data = np.fromfile(data_2, dtype=np.uint32)
data = data.tolist()
print("data:", len(data))

EXPECTED = [2.103, 5.779, 17.554, 46.732, 110.783,
            236.784, 460.944, 824.116, 1362.781, 2096.849,
            3017.612, 4080.197, 5204.203, 6283.828, 7205.637,
            7869.451, 8206.755, 8191.935, 7844.008, 7219.412,
            6398.679, 5470.931, 4519.852, 3613.661, 2800.028,
            2105.567, 1538.652, 1094.02, 757.796, 511.956,
            337.726, 217.787, 137.439, 84.97, 51.518,
            30.666, 17.939, 10.324, 5.851, 3.269,
            1.803, 0.982, 1.121]

NO_TESTS = 10

p_vals = []
chi_sqs = []

temp = 0
for test in range(NO_TESTS):
    j_freqs = [0] * 43
    for test_number in range(100000):
        k = 2147483648
        j = 0
        while k != 1 and j <= 48:
            k = math.ceil(k * random.random())
            j += 1
        if 6 <= j <= 48:
            j_freqs[j - 6] += 1
        elif j < 6:
            j_freqs[0] += 1
        else:
            j_freqs[42] += 1

    #print(j_freqs)

    #chi_sq = 0
    #for i in range(len(j_freqs)):
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
print("Passed " + str(per_count) + " out of " + str(NO_TESTS) + " (" + str(per_count/NO_TESTS*100) + "%) tests")
#result = stats.kstest(p_vals, 'uniform')

#Wprint(result)