import numpy as np
import scipy
import scipy as sp
import math
import audioop
import pydub
import binascii

# S - latest sample - variable name - cur_s
# SP - last sample - prev_s
# SPP - sample before last one - pp_s

# n - amount of samples
# n__th - correspondent sample
# same for SP_n and SPP_n

from matplotlib import pyplot as plt
from scipy.io import wavfile

wilczur = 10
if wilczur == 10:
    print("poka wilczura joł")


f_name= "white_noise_final2.wav"
rate, data = sp.io.wavfile.read(f_name)

for i in data:
    print(data)

