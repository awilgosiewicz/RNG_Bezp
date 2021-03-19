import numpy as np
import scipy
import scipy as sp
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import stats
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


f_name= "white_noise_final2.wav"
rate, data = sp.io.wavfile.read(f_name)
bins=255

figAudio, his = plt.subplots()
his.hist([data],bins,range=[0,255])
sp.stats.entropy(data, base=None) #nie wiem co z tym base, bo może być 2 a może być None, muszę o tym doczytać

