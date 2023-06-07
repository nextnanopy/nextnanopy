import shapely
import shapely.geometry
import shapely.ops
import matplotlib.pyplot as plt
import numpy as np


class SlicedPolygon(shapely.geometry.Polygon):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._slices = []
        self.slice()

    @property
    def bounds_x(self):
        return np.array([self.bounds[0], self.bounds[2]])

    @property
    def bounds_y(self):
        return np.array([self.bounds[1], self.bounds[3]])

    @property
    def x(self):
        return np.array(self.boundary.xy[0])

    @property
    def y(self):
        return np.array(self.boundary.xy[1])

    @property
    def x_unique(self):
        return np.unique(self.x)

    @property
    def y_unique(self):
        return np.unique(self.y)

    @property
    def slice_axis(self):
        if len(self.x_unique) <= len(self.y_unique):
            axis = 'x'
        else:
            axis = 'y'
        return axis

    @property
    def slice_points(self):
        if self.slice_axis == 'x':
            arr = self.x_unique
        elif self.slice_axis == 'y':
            arr = self.y_unique
        points = np.copy(arr[1:-1])
        return points

    @property
    def sliceable(self):
        boolean = True
        if not list(self.slice_points):
            boolean = False
        return boolean

    @property
    def slice_line(self):
        if self.slice_axis == 'x':
            index = 0
            bounds = self.bounds_y
        else:
            index = 1
            bounds = self.bounds_x
        points = []
        for i, si in enumerate(self.slice_points):
            # -- For each slice point, we need to create 2 points
            point = [0, 0]
            point[index] = si
            point[(index + 1) % 2] = bounds[i % 2]
            points.append(list(point))
            point[index] = si
            point[(index + 1) % 2] = bounds[(i + 1) % 2]
            points.append(list(point))
        return shapely.geometry.LineString(points)

    @property
    def slices(self):
        return self._slices

    def slice(self):
        if not self.sliceable:
            slices = [self]
        else:
            slices = shapely.ops.split(self, self.slice_line)
        self._slices = slices
        return slices

    def correct_xy(self):
        xs, ys = [], []
        for polygon in self.slices:
            x, y = np.array(polygon.boundary.xy)
            x, y = self._remove_redundant_vertexes(x, y)
            x, y = self._correct_xy_for_triangles(x, y)
            x, y = self._order_xy_for_nn(x, y)
            xs.append(x)
            ys.append(y)
        return xs, ys

    def _remove_redundant_vertexes(self, x, y, remove_last_point=True):
        xy = np.array([x, y])
        xy = np.transpose(xy)
        if remove_last_point and (xy[0] == xy[-1]).all():  # remove the last point (repeated)
            xy = np.delete(xy, -1, axis=0)
        idx_to_delete = []
        nb_points = xy.shape[0]
        for i in range(nb_points):
            i_l = i - 1
            i_m = i
            i_r = int((i + 1) % nb_points)
            xy_l = xy[i_l]
            xy_m = xy[i_m]
            xy_r = xy[i_r]
            v1 = xy_m - xy_l
            v2 = xy_r - xy_m
            if np.cross(v1, v2) == 0:
                idx_to_delete.append(i)
        # -- Delete indexes
        # -- Note that you need to delete them in reverse order so that you don't throw off the subsequent indexes.
        for ind in sorted(idx_to_delete, reverse=True):
            xy = np.delete(xy, ind, axis=0)
        xy = np.transpose(xy)
        x, y = xy
        return x, y

    def _correct_xy_for_triangles(self, x, y):
        nb_vertexes = len(x)
        if nb_vertexes == 3:  # it is a triangle
            if self.slice_axis == 'x':
                p_check = x
            elif self.slice_axis == 'y':
                p_check = y

            if p_check[0] == p_check[1]:
                duplicate_index = 2
            elif p_check[0] == p_check[2]:
                duplicate_index = 1
            else:
                duplicate_index = 0

            x = np.append(x, x[duplicate_index])
            y = np.append(y, y[duplicate_index])
        return x, y

    def _order_xy_for_nn(self, x, y):
        if self.slice_axis == 'x':
            p_sort = x
            p_follow = y
        elif self.slice_axis == 'y':
            p_sort = y
            p_follow = x

        p_sorted = np.sort(p_sort)
        arg_sorted = np.argsort(p_sort)
        p_follow = p_follow[arg_sorted]

        if self.slice_axis == 'x':
            x = p_sorted
            y = p_follow
        elif self.slice_axis == 'y':
            y = p_sorted
            x = p_follow
        return x, y

    def show_slices(self, ax=None, fill_kw={}):
        if not ax:
            fig, ax = plt.subplots(1)
        ax.set_xlabel(f'x')
        ax.set_ylabel(f'y')
        for pol in self.slices:
            x, y = pol.boundary.xy
            ax.fill(x, y, **fill_kw)
        return ax