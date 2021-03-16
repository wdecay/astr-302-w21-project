import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from solar import SolarSystem
import time

def initialize_matplotlib():
    matplotlib.use('Agg')
    plt.style.use('dark_background')


def generate_plot(nmax, data):
    ss = SolarSystem(data)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_aspect(1)
    f = 0.05 if nmax >= 7 else 1
    ax.scatter(0, 0, s=f*200, zorder=100, color='tab:orange')
    colors = ['tab:brown', 'tab:olive', 'tab:blue', 'tab:red',
        'tab:purple', 'tab:pink', 'tab:green', 'tab:cyan']
    names = []
    for n in range(1, nmax):
        tic = time.perf_counter()

        r0, coords, name = ss.get_planet(n)
        toc = time.perf_counter()
        print("Latency: {:.3f}s".format(toc - tic))
        fp = f if n < 5 else 1
        ax.plot(coords[:, 0], coords[:, 1], ':', lw=max(fp, 0.2), color='white')
        ax.scatter(r0[0], r0[1], s=fp*30, zorder=100, color=colors[n-1], marker='o', label=name)
        names.append(name)
    ax.set_xlabel('AU')
    ax.set_ylabel('AU')
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.grid(True, linewidth=0.1)
    fig.tight_layout()
    return fig

def close_fig(fig):
    plt.close(fig)