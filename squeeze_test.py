import random
import math


numbers = []
for _ in range(5000000):
    numbers.append(random.random())

number_used = 0
j_values = [0] * 48
for test_number in range(100000):
    k = 2147483648
    j = 0
    while k != 1 and j <= 48:
        k = math.ceil(k * numbers[number_used])
        number_used += 1
        j += 1
    if 6 <= j <= 48:
        j_values.append(j)

print(j_values)
print(len(j_values))
