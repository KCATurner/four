import numpy as np
import matplotlib.pyplot as plt
from four._oo_method import *


if __name__ == '__main__':

    target_zillions, number_zillions = [], []
    for num_periods in range(1, 51):
        target = PeriodList([Period(373, num_periods)])
        number = number_from_name_length(target=target, debug=False)
        number_zillions.append(sum((r for _, r in number)))
        target_zillions.append(sum((r for _, r in target)))

        print(f"target: {target}\tnumber: {number}")

    x = np.array(target_zillions)
    y = np.array(number_zillions)

    print(x, y, sep="\n")
    exit()

    theta = np.polyfit(x, y, 2)
    curve = np.poly1d(theta)
    error = y - curve(x)

    # print(theta)
    # print(curve)

    plt.errorbar(x, y, yerr=error, fmt='+', ecolor='r', label='data')
    plt.plot(x, curve(x), 'r-', scalex=False, scaley=False, label=curve)
    plt.legend(loc='upper left')

    plt.show()
