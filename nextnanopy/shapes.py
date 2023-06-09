import numpy as np
import matplotlib.pyplot as plt
from cycler import cycler
import gdspy
import warnings

units_factor = {
    'nm': 1e-9,
    'um': 1e-6,
    'mm': 1e-3,
    'm': 1,
    'si': 1,
}


def validate_unit(key):
    key = str(key).lower()
    if key not in units_factor.keys():
        raise KeyError(f'Invalid unit: {key}')
    return True


class GdsPolygonsRaw(object):
    def __init__(self, fullpath, unit='nm', **kwargs):
        self.fullpath = fullpath
        self._labels = []
        self._unit = 'm'
        self.load(**kwargs)
        self.unit = unit
        self.added_labels = []

    @property
    def xy(self):
        _xy = [np.array(pol_xy).transpose() for pol_xy in self.polygons_xy]
        return _xy

    @property
    def unit(self):
        return self._unit

    @unit.setter
    def unit(self, key):
        validate_unit(key)
        self.polygons_xy = [xy * units_factor[self._unit] / units_factor[key]
                            for xy in self.polygons_xy]
        self._unit = key

    @property
    def labels(self):
        return self._labels

    @labels.setter
    def labels(self, names):
        if len(names) == self.nb_polygons:
            self._labels = names
        else:
            print(f'Number of label ({names}) must be equal to number of polygons ({self.nb_polygons})')
            print(f'Using default labels: {self.labels}')

    @property
    def nb_polygons(self):
        return len(self.polygons_xy)

    def load(self, **kwargs):
        self.load_polygons_xy(**kwargs)
    @property
    def slices(self):
        warnings.warn("The GdsPolygonsRaw.slices is deprecated",DeprecationWarning)
        from nextnanopy.utils.shapes_deprecated import SlicedPolygon
        return [SlicedPolygon(pol_xy) for pol_xy in self.polygons_xy]

    def load(self):
        self.load_polygons_xy()
        self.set_default_labels()

    def load_polygons_xy(self, **kwargs):
        gds_lib = gdspy.GdsLibrary(infile=self.fullpath)
        xys = []
        if 'by_spec' not in kwargs:
            kwargs['by_spec'] = False
        for cell in gds_lib.top_level():
            pols = cell.get_polygons(kwargs['by_spec'])
            pols = [pi * gds_lib.unit for pi in pols]
            xys.extend(pols)
        self.polygons_xy = xys
        return xys

    def set_default_labels(self):
        if len(self.labels) == 0:
            self.labels = np.arange(self.nb_polygons)

    # -- Useful show methods
    def _prepare_ax(self, ax=None, cmap='nipy_spectral'):
        plt.ion()
        if not ax:
            fig, ax = plt.subplots(1)
        if cmap:
            colormap = plt.get_cmap(cmap)
            colors = [colormap(i) for i in np.linspace(0, 1, self.nb_polygons)]
            ax.set_prop_cycle(cycler('color', colors))
        ax.set_xlabel(f'x {self.unit}')
        ax.set_ylabel(f'y {self.unit}')
        return ax

    def show_all(self, ax=None, cmap='nipy_spectral', fill_kw={}):
        ax = self._prepare_ax(ax, cmap)
        for xy, label in zip(self.xy, self.labels):
            x, y = xy
            ax.fill(x, y, label=label, **fill_kw)
        ax.legend(loc='upper right')
        return ax

    def show_onebyone(self, ax=None, cmap='nipy_spectral', fill_kw={}):
        ax = self._prepare_ax(ax, cmap)
        for pol, label in zip(self.polygons, self.labels):
            x, y = pol.boundary.xy
            ax.fill(x, y, color='grey', alpha=0.5)
        for pol, label in zip(self.polygons, self.labels):
            x, y = pol.boundary.xy
            ax.fill(x, y, label=label, **fill_kw)
            ax.legend(loc='upper right')
            ax.figure.canvas.draw()
            print('Do you want to continue? (enter = yes, any other key = no)')
            answer = input().lower()
            if answer != '':
                break
        return ax

    def show(self, ax=None, cmap='nipy_spectral', fill_kw={}, onebyone=False):
        if onebyone:
            ax = self.show_onebyone(ax, cmap, fill_kw)
        else:
            ax = self.show_all(ax, cmap, fill_kw)
        return ax

    def show_slices(self, ax=None, fill_kw={}):
        ax = self._prepare_ax(ax, cmap=None)
        for spol in self.slices:
            for pol in spol.slices:
                x, y = pol.boundary.xy
                ax.fill(x, y, **fill_kw)
        return ax

    def show_polygon(self, polygon, label, ax=None, cmap='nipy_spectral', fill_kw={}):
        # print(f"Polygon:  {polygon}")
        # print(f"Label:  {label}")
        ax = self._prepare_ax(ax, cmap)
        for _ in polygon:
            x, y = zip(*polygon)
            ax.fill(x, y, label=label, **fill_kw)
        # if label not in self.added_labels:
        #     ax.legend(loc='upper right')
        #     self.added_labels.append(label)
        return ax
