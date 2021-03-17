"""
Matplotlib initialization and plot rendering functions.
"""

import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from solar import SolarSystem

def initialize_matplotlib():
    """
    One-time initialization of a non-GUI matplotlib backend
    and global dark background style.
    """ 
    matplotlib.use('Agg')
    plt.style.use('dark_background')


def generate_plot(date, n):
    """
    Generation of a 2D plot with the Sun and <n> planets 
    (the z coordinate representing the inclination is ignored)

    Parameters:
        date: in the `yyyy-mm-dd` format
        n: limit on the number of planets to render (e.g.,., 4 to go up to Mars)

    Returns:
        matplotlib.figure.Figure object
    """
    ss = SolarSystem(date)
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_aspect(1)
    f = 0.05 if n >= 6 else 1 # scale factor
    ax.scatter(0, 0, s=f*200, zorder=100, color='tab:orange') # Sun
    # color palette for the planets
    colors = ['tab:brown', 'tab:olive', 'tab:blue', 'tab:red',
        'tab:purple', 'tab:pink', 'tab:green', 'tab:cyan']
    names = []
    for i in range(1, n + 1):
        r0, coords, name = ss.get_planet(i)
        f_inner = f if i < 5 else 1 # scale factor for inner planets
        ax.plot(coords[:, 0], coords[:, 1], ':', lw=max(f_inner, 0.2), color='white')
        ax.scatter(r0[0], r0[1],
                   s=f_inner*30, zorder=100, color=colors[i-1], marker='o', label=name)
        names.append(name)
    ax.set_xlabel('AU')
    ax.set_ylabel('AU')
    ax.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    ax.grid(True, linewidth=0.1)
    fig.tight_layout()
    return fig

def close_fig(fig):
    """Closes the figure to make sure memory is released.
    """
    plt.close(fig)
