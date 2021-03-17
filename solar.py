"""
Solar system model.
The idea of the Euler integration method for calculating the orbits was taken from
https://medium.com/analytics-vidhya/simulating-the-solar-system-with-under-100-lines-of-python-code-5c53b3039fc6
"""

import numpy as np
import numba as nb
from astropy.time import Time
from astroquery.jplhorizons import Horizons

@nb.jit(nopython=True)
def compute_orbit(r, v, dt, tmax):
    """
    Numba-accelerated Euler integration to calculate planets' obrits.
    Note: Numba doesn't work with class methods, so this had to be implemented
    as a standalone function.

    Parameters:
        r: initial position (AU)
        v: initial velocity (AU/day)
        dt: time step (days)
        tmax: integration interval (days)

    Returns:
        Calculated orbit as a numpy array of 3D points
    """
    niter = int(tmax / dt)
    coords = np.empty((niter, 3))
    for i in range(0, niter):
        r += v * dt
        # GM = 6.6743e-11 * 1.9885e30 * (1/1.4960e11)**3 * (60*60*24)**2 = 2.959e-4 AU^3/day^2
        acc = -2.959e-4 * r / np.sqrt(np.sum(r**2))**3
        v += acc * dt
        coords[i, :] = r
    return coords

class SolarSystem:
    """
    Basic solar system model.
    """
    def __init__(self, date):
        """
        Constructor.

        Parameters:
            date: `yyyy-mm-dd` format date
        """
        self.__t0 = Time(date).jd

    def get_planet(self, n):
        """
        Nth planet info.

        Parameters:
            n: planet number (Mercury is 1, etc.)
        
        Returns:
            Tuple consisting of the
            r0: current coordinates (AU)
            orbit: calculated orbit
            name: name of the planet
        """
        obj = Horizons(id=n, location="@sun", epochs=self.__t0, id_type='id')
        r0 = np.array([float(obj.vectors()[xn]) for xn in ['x', 'y', 'z']])
        v = np.array([float(obj.vectors()[xn]) for xn in ['vx', 'vy', 'vz']])
        r = np.copy(r0)
        tmax = np.double(obj.elements()['P']) # orbital period (days)
        dt = tmax / 400 # seems like an OK compromise between accuracy and performance
        orbit = compute_orbit(r, v, dt, tmax)
        name = obj.vectors()['targetname'].data[0].split()[0] # extracts the name of planet
        return r0, orbit, name
