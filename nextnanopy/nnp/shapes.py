from nextnanopy.nnp.assistants import InputAssistant
from collections import OrderedDict
from nextnanopy.shapes import GdsPolygonsRaw
import numpy as np
import warnings

class GdsPolygons(GdsPolygonsRaw):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get_obelisks(self, zi, zf):
        warnings.warn("The usage of get_obelisks is deprecated. Please, GdsPolygons.get_polygonal_prisms instead", DeprecationWarning)
        shapes = []
        z = np.array([zi, zf] * 2)
        for si in self.slices:
            xs, ys = si.correct_xy()
            for x, y in zip(xs, ys):
                kwargs = {
                    'base_x': x[:2],
                    'base_y': y[:2],
                    'base_z': z[:2],
                    'top_x': x[2:],
                    'top_y': y[2:],
                    'top_z': z[2:],
                }
                shapes.append(Obelisk(**kwargs))
        return shapes

    def get_polygonal_prisms(self, zi, zf):
        z = np.array([zi, zf])
        axes = ['x', 'y', 'z']
        shapes = [Polygonal_prism(axes=axes, vertexes=xy, height=z) for xy in
                  self.polygons_xy]
        return shapes


class Shape(object):
    def __init__(self):
        self._ia = InputAssistant()

    @property
    def text(self):
        return ''

    @property
    def preview(self):
        self._ia.preview(self.text, nums=False)


class Obelisk(Shape):

    def __init__(self, base_x, base_y, base_z, top_x, top_y, top_z):
        super().__init__()
        self.base_x = base_x
        self.base_y = base_y
        self.base_z = base_z
        self.top_x = top_x
        self.top_y = top_y
        self.top_z = top_z

    @property
    def text(self):
        return self._ia.region_obelisk(**self.kwargs)

    @property
    def kwargs(self):
        _kwargs = OrderedDict()
        keys = ['base_x', 'base_y', 'base_z', 'top_x', 'top_y', 'top_z']
        for key in keys:
            if key not in dir(self):
                raise KeyError(f'{key} is not defined in the attributes')
            else:
                _kwargs[key] = getattr(self, key)
        return _kwargs


class Polygonal_prism(Shape):

    def __init__(self, axes=['x', 'y', 'z'], vertexes=[[10.5, 14.0]],
                 height=[0, 10]):
        super().__init__()
        self.axes = axes
        self.vertexes = vertexes
        self.height = height

    @property
    def text(self):
        return self._ia.region_polygonal_prism(**self.kwargs)

    @property
    def kwargs(self):
        _kwargs = OrderedDict()
        keys = ['axes', 'vertexes', 'height']
        for key in keys:
            if key not in dir(self):
                raise KeyError(f'{key} is not defined in the attributes')
            else:
                _kwargs[key] = getattr(self, key)
        return _kwargs
