import numpy as np
from scipy.optimize import curve_fit
from matplotlib import pyplot as plt

from four import infer


def integer_exact(x, a):
    return np.array([
        float(('373' * int(i)) or 0.0) / a
        for i in x])


def integer_approx(x, a):
    return np.array([
        float(373 * (1000 ** int(i))) / a
        for i in x])


def float_exact(x, a, b):
    return np.array([
        a * (float(('373' * int(i)) or 0.0) ** b)
        for i in x])


def float_approx(x, a, b):
    return np.array([
        a * (float(373 * (1000 ** int(i))) ** b)
        for i in x])


if __name__ == '__main__':
    xdata = np.arange(80)
    ydata = np.array(infer.LENGTH_PERIODS_TO_TARGET_PERIODS)

    fig, ax = plt.subplots(2, 2, sharex='all', sharey='all')
    for index, func in enumerate([
        integer_exact,
        integer_approx,
        float_exact,
        float_approx,
    ]):
        axis = ax[divmod(index, 2)]
        pivot = len(ydata)

        popt, *_ = curve_fit(func, xdata[:pivot], ydata, full_output=True)
        predictions = func(xdata, *popt)
        error = abs(predictions[:pivot] - ydata)

        axis.plot(xdata[:pivot], ydata, 'ko', label="Original Data", zorder=10)
        axis.plot(xdata[pivot:], predictions[pivot:], 'bo', label="Predictions", zorder=10)

        axis.plot(xdata, predictions, 'k-', label=f"Fitted Curve (popt = {popt})", zorder=20)
        axis.errorbar(xdata[:pivot], ydata, yerr=error, fmt="r|", label="Curve Error", zorder=0)

        axis.set_title(func.__name__)
        axis.set_xscale('log')
        axis.set_yscale('log')
        axis.legend()

    mng = plt.get_current_fig_manager()
    mng.window.state('zoomed')
    plt.show()
