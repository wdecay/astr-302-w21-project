import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from solar import SolarSystem

def generate_plot(nmax, data):
    matplotlib.use('Agg')

    ss = SolarSystem(data)
    fig, ax = plt.subplots(figsize=(10, 8), num='dark_background')
    plt.style.use('dark_background')
    ax.set_aspect(1)
    f = 0.1 if nmax >= 7 else 1
    ax.scatter(0, 0, s=f*400, zorder=100, color='tab:orange')
    colors = ['tab:brown', 'tab:olive', 'tab:blue', 'tab:red',
        'tab:purple', 'tab:pink', 'tab:green', 'tab:cyan']
    names = []
    for n in range(1, nmax):
        r0, coords, name = ss.get_planet(n)
        fp = f if n < 5 else 1
        ax.plot(coords[:, 0], coords[:, 1], ':', lw=fp*1.2, color='white')
        
        ax.scatter(r0[0], r0[1], s=f*170, zorder=100, color=colors[n-1], marker='o', label=name)
        names.append(name)
    ax.set_xlabel('AU')
    ax.set_ylabel('AU')
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.grid(True, linewidth=0.2)
    fig.tight_layout()
    return fig

def close_fig(fig):
    plt.close(fig)