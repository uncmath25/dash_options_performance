import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

PLOT_FILE = 'temp.png'

def build_sample_line_plot():
    plt.rcParams["figure.figsize"] = (16, 9)
    x = list(range(100 + 1))
    y = [0.5 for _ in x]
    plt.scatter(x, y, color='blue')
    plt.plot([0, 100], [0, 1], color='green')
    axes = plt.gca()
    axes.set_xlim([0, 100])
    axes.set_ylim([0, 1])
    plt.title('Sample Plot')
    plt.xlabel('x')
    plt.ylabel('y')
    plt.savefig(PLOT_FILE)
    plt.clf()

build_sample_line_plot()
