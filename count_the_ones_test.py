from collections import Counter
import numpy as np
import scipy.stats
import random


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


data_2 = open("fortnite.bin", "rb") #rb musi być niby
data = np.fromfile(data_2, dtype=np.uint32)
array = []
words = []
words5 = []
words4 = []


for number in range(256000):
    array.append(int(random.random()*255.0))

i = 0
while i < len(array) - 4:
    #ilość jedynek liczb
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
while i < len(array) - 3:
    #ilość jedynek liczb
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

print(words5)
print(words4)

x5 = len(words5)
x4 = len(words4)
print(x5)
print(x4)

print(len(set(words5)))
print(len(set(words4)))

number_of_appearances5 = Counter(words5)
number_of_appearances4 = Counter(words4)
#print(number_of_appearances5)
#print(number_of_appearances4)


prob5 = []
for x in number_of_appearances5:
    prob5.append(number_of_appearances5.get(x))

prob4 = []
print(len(number_of_appearances4))
for x in number_of_appearances4:
    prob4.append(number_of_appearances4.get(x))

chi5 = scipy.stats.chi2_contingency(prob5)
chi4 = scipy.stats.chi2_contingency(prob4)

print(chi5)
print(chi4)
