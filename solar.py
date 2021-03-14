import numpy as np
from astropy.time import Time
from astroquery.jplhorizons import Horizons

class SolarSystem:
    def __init__(self, date):
        self.__t0 = Time(date).jd

    def get_planet(self, n):
        obj = Horizons(id=n, location="@sun", epochs=self.__t0, id_type='id')

        r0 = np.array([obj.vectors()[xn] for xn in ['x', 'y', 'z']])
        v = np.array([obj.vectors()[xn] for xn in ['vx', 'vy', 'vz']])
        r = np.copy(r0)
        tmax = np.double(obj.elements()['P'])
        t = 0
        dt = tmax / 400
        coords = []
        while t < tmax:
            r += v * dt
            acc = -2.959e-4 * r / np.sqrt(np.sum(r**2))**3
            v += acc * dt
            t += dt
            coords.append(r.flatten())
        coords = np.array(coords)
        return r0, coords, obj.vectors()['targetname'].data[0].split()[0]
