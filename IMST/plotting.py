
import math
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
import statistics as st

def plot_means_comparative(lists, plot_title="", plot_ylabel=""):

    means = []
    stdevs = []

    names = ["Слика лево", "Слика десно", "Без одговарајуће слике"]
    x_pos = np.arange(len(names))

    for i in range(len(lists)):
        to_plot = lists[i]
        means.append(st.mean(to_plot))
        stdevs.append(st.stdev(to_plot))

    low = min([means[i] - stdevs[i] for i in range(len(means))])
    high = max([means[i] + stdevs[i] for i in range(len(means))])
    low = min([low, -0.1*high])

    fig, ax = plt.subplots()
    ax.bar(names, means, yerr=stdevs, align='center', color="#1a0961", alpha=0.9, ecolor='firebrick', capsize=10)
    ax.set_ylim([math.ceil(low - 0.1 * (high - low)), math.ceil(high + 0.1 * (high - low))])
    ax.set_ylabel(plot_ylabel)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(names)
    ax.set_title(plot_title)
    ax.yaxis.grid(True)

    plt.tight_layout()
    fig.set_size_inches(8, 6)
    plt_name = plot_title + ".png"
    plt.savefig(plt_name, dpi=100)
    plt.show()


if __name__ == '__main__':

    data = pd.read_csv("Results.csv")
    rights = data[data["Stimulus"] == "right"]
    lefts = data[data["Stimulus"] == "left"]
    nones = data[data["Stimulus"] == "None"]

    divided_data = [lefts, rights, nones]

    x_dispersion = []
    y_dispersion = []
    no_of_clusters = []
    no_of_saccades = []

    for dt in divided_data:
        x_dispersion.append(dt["Dispersion X"].tolist())
        y_dispersion.append(dt["Dispersion Y"].tolist())
        no_of_clusters.append(dt["No. of Clusters"].tolist())
        no_of_saccades.append(dt["No. of Saccades"].tolist())

    plot_means_comparative(x_dispersion, "Дисперзија појединачних кластера по х-оси", "px")
    plot_means_comparative(y_dispersion, "Дисперзија појединачних кластера по y-оси", "px")
    plot_means_comparative(no_of_clusters, "Број кластера у односу на позицију стимулуса на екрану")
    plot_means_comparative(no_of_saccades, "Број сакада у односу на позицију стимулуса на екрану")

