import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from solar import SolarSystem

def generate_plot(nmax, data):
    matplotlib.use('Agg')

    ss = SolarSystem(data)
    plt.figure(figsize=(10,8))
    plt.style.use('dark_background')
    axes=plt.gca()
    axes.set_aspect(1)
    f = 0.1 if nmax >= 7 else 1
    plt.scatter(0, 0, s=f*400, color='tab:orange')
    colors = ['tab:brown', 'tab:olive', 'tab:blue', 'tab:red',
    'tab:purple', 'tab:pink', 'tab:green', 'tab:cyan']
    names = []
    for n in range(1, nmax):
        r0, coords, name = ss.get_planet(n)
        fp = f if n < 5 else 1
        plt.plot(coords[:, 0], coords[:, 1], ':', lw=fp*1.2, color='white')
        
        plt.scatter(r0[0], r0[1], s=f*170, zorder=100, color=colors[n-1], marker='o', label=name)
        names.append(name)
    plt.xlabel('AU')
    plt.ylabel('AU')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid(True, linewidth=0.2)
    plt.tight_layout()
    return plt
