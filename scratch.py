import numpy as np
import matplotlib.pyplot as plt
from four._oo_method import *


if __name__ == '__main__':

    repeats, lengths = [], []
    for seed in range(1200):
        repeat = seed*1
        number = PeriodList([Period(373, repeat)])
        length = number.name_length
        repeats.append(int(repeat))
        lengths.append(int(length))

    x = np.array(repeats)
    y = np.array(lengths)
    c = np.poly1d(np.polyfit(x, y, 1))
    e = y - c(x)

    plt.errorbar(x, y, yerr=e, fmt='+', ecolor='r', label='data')
    plt.plot(x, c(x), 'r-', label='trend')
    plt.legend(loc='upper left')

    # me = max(list(e.flatten())[200:])
    # mei = list(e.flatten())[200:].index(me)
    # mex = repeats.index(mei)
    # mey = lengths[mex]
    # plb.plot(np.array([mex, ]), np.array([mey, ]), label='max error',)

    plt.show()
