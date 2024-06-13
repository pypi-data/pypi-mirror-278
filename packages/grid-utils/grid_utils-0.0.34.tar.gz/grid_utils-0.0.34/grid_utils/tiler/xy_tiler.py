# -*- coding:utf-8 -*-

import six
import numpy as np
from functools import reduce
from operator import add

__all__ = ['XYTiler']


class XYTiler(object):
    _offset_dict = {
        "center": (0.5, 0.5),
        "lowerleft": (0.0, 0.0),
        "lowerright": (1.0, 0.0),
        "upperleft": (0.0, 1.0),
        "upperright": (1.0, 1.0)
    }

    def __init__(self, x_size, y_size, nx, ny, x0=0.0, y0=0.0, margin=0, i_min=None, i_max=None, j_min=None, j_max=None, circular_xs=None, **kwargs):
        """

        :param x_size:
        :param y_size:
        :param nx:
        :param ny:
        :param x0:
        :param y0:
        :param margin:
        :param i_min:
        :param i_max:
        :param j_min:
        :param j_max:
        :param circular_xs: None or [x1, x2] (e.g. [-180.0, 180.0])
        :param kwargs:
        """
        self.x_size = x_size
        self.y_size = y_size

        self.nx = nx
        self.ny = ny

        self.x0 = x0
        self.y0 = y0

        self.dx = self.x_size / self.nx
        self.dy = self.y_size / self.ny

        self.margin = margin

        self.i_min = i_min
        self.i_max = i_max
        self.j_min = j_min
        self.j_max = j_max

        self.circular_xs = circular_xs

    @property
    def full_nx(self):
        return self.nx + self.margin * 2

    @property
    def full_ny(self):
        return self.ny + self.margin * 2

    def xy2tile(self, x, y, margin=True, ignore_circular=False):
        if not ignore_circular:
            x = self.circular_shift(x)
        tile_i, i = self._to_tile_1d(x, self.x0, self.x_size, self.nx)
        tile_j, j = self._to_tile_1d(y, self.y0, self.y_size, self.ny)
        if margin:
            i += self.margin
            j += self.margin
        return tile_i, tile_j, i, j

    def tile2xy(self, tile_i, tile_j, i, j, pos='center', margin=True):
        i_offset, j_offset = self._offset_dict.get(pos, (0.5, 0.5))
        if margin:
            i -= self.margin
            j -= self.margin
        x = self._to_xy_1d(tile_i, i, self.x0, self.x_size, self.nx, i_offset)
        y = self._to_xy_1d(tile_j, j, self.y0, self.y_size, self.ny, j_offset)
        return x, y

    def get_tile_xys(self, tile_i, tile_j, pos='center', margin=True):
        i_offset, j_offset = self._offset_dict.get(pos, (0.5, 0.5))
        if margin:
            ii = np.arange(-self.margin, self.nx+self.margin)
            jj = np.arange(-self.margin, self.ny+self.margin)
        else:
            ii = np.arange(self.nx)
            jj = np.arange(self.ny)
        xs = self._to_xy_1d(tile_i, ii, self.x0, self.x_size, self.nx, i_offset)
        ys = self._to_xy_1d(tile_j, jj, self.y0, self.y_size, self.ny, j_offset)
        return xs, ys

    def get_tile_bbox(self, tile_i, tile_j):
        x1 = self.x0 + self.x_size * tile_i
        y1 = self.y0 + self.y_size * tile_j
        x2 = x1 + self.x_size
        y2 = y1 + self.y_size
        return (x1, y1, x2, y2)

    def circular_shift(self, x):
        if not self.circular_xs:
            return x
        cx1, cx2 = self.circular_xs

        if x < cx1:
            return x + (cx2 - cx1)
        elif x >= cx2:
            return x - (cx2 - cx1)
        else:
            return x

    def circular_shift_xs(self, x1, x2, direction=None):
        if not self.circular_xs:
            return x1, x2
        cx1, cx2 = self.circular_xs
        span = cx2 - cx1

        if direction == 'right':
            return x1 + span, x2 + span
        elif direction == 'left':
            return x1 - span, x2 - span
        else:
            return x1, x2

    def get_circular_tile_i(self, tile_i):
        if not self.circular_xs:
            return None
        cx1, cx2 = self.circular_xs

        total_n_ti = int(np.round(360.0 / self.x_size))
        cti1 = int(np.round((cx1 - self.x0) / float(self.x_size)))
        center_ti = cti1 + total_n_ti / 2
        if tile_i >= center_ti:
            return tile_i - total_n_ti
        else:
            return tile_i + total_n_ti

    def get_covered_tiles(self, x1, y1, x2, y2, padding=0, detail=False, margin=True, circular_handled=False):
        if self.circular_xs and not circular_handled:
            cx1, cx2 = self.circular_xs

            # split range [x1, x2] into several parts
            parts = []
            rest_x1 = x1
            while rest_x1 is not None:
                if rest_x1 < cx1:
                    if x2 <= cx1:
                        parts.append(self.circular_shift_xs(rest_x1, x2, direction='right'))
                        break
                    else:
                        parts.append(self.circular_shift_xs(rest_x1, cx1, direction='right'))
                        rest_x1 = cx1
                elif rest_x1 < cx2:
                    if x2 <= cx2:
                        parts.append((rest_x1, x2))
                        break
                    else:
                        parts.append((rest_x1, cx2))
                        rest_x1 = cx2
                else:
                    parts.append(self.circular_shift_xs(rest_x1, x2, direction='left'))
                    break

            part_results = [self.get_covered_tiles(px1, y1, px2, y2, padding=padding, detail=detail, margin=margin, circular_handled=True) for (px1, px2) in parts]

            if detail:
                final_result = {
                    'nj': part_results[0]['nj']
                }

                for key in ['ni', 'tile_list']:
                    value_list = [pr[key] for pr in part_results]
                    final_result[key] = reduce(add, value_list)

                def merge_dict(a, b):
                    a.update(b)
                    return a

                for key in ['i_beg_dict', 'i_end_dict', 'j_beg_dict', 'j_end_dict', 'j_offset_dict']:
                    value_list = [pr[key] for pr in part_results]
                    final_result[key] = reduce(merge_dict, value_list, {})

                offoff = 0
                final_i_offset_dict = {}
                for pr in part_results:
                    for k, v in pr['i_offset_dict'].items():
                        final_i_offset_dict[k] = v + offoff
                    offoff += pr['ni']

                final_result['i_offset_dict'] = final_i_offset_dict

                # when generating total_xs and total_ys, circular is not considered.
                tile_i1, tile_j1, i1, j1 = self.xy2tile(x1, y1, margin=False, ignore_circular=True)
                tile_i2, tile_j2, i2, j2 = self.xy2tile(x2, y2, margin=False, ignore_circular=True)
                x_beg, y_beg = self.tile2xy(tile_i1, tile_j1, i1, j1, margin=False)
                x_end, y_end = self.tile2xy(tile_i2, tile_j2, i2, j2, margin=False)
                total_xs = np.linspace(x_beg, x_end, final_result['ni'])
                total_ys = np.linspace(y_beg, y_end, final_result['nj'])
                final_result.update({
                    "xs": total_xs,
                    "ys": total_ys,
                })
            else:
                final_result = []
                for part_result in part_results:
                    final_result.extend(part_result)

            return final_result

        # margin is considered only when generating each tile's details.
        tile_i1, tile_j1, i1, j1 = self.xy2tile(x1, y1, margin=False, ignore_circular=True)
        tile_i2, tile_j2, i2, j2 = self.xy2tile(x2, y2, margin=False, ignore_circular=True)

        x2_, y2_ = self.tile2xy(tile_i2, tile_j2, i2, j2, pos='lowerleft', margin=False)
        if i2 == 0:
            if x2 < x2_ + (self.x_size / self.nx) / 10.0:
                tile_i2 -= 1
                i2 = self.nx - 1
        if j2 == 0:
            if y2 < y2_ + (self.y_size / self.ny) / 10.0:
                tile_j2 -= 1
                j2 = self.ny - 1

        # Add padding
        i1 -= padding
        i2 += padding
        j1 -= padding
        j2 += padding

        tile_i1 += i1 // self.nx
        tile_i2 += i2 // self.nx
        tile_j1 += j1 // self.ny
        tile_j2 += j2 // self.ny

        i1 %= self.nx
        i2 %= self.nx
        j1 %= self.ny
        j2 %= self.ny

        if self.i_min is not None and tile_i1 < self.i_min:
            tile_i1 = self.i_min
            i1 = 0
        if self.i_max is not None and tile_i2 > self.i_max:
            tile_i2 = self.i_max
            i2 = self.nx - 1

        if self.j_min is not None and tile_j1 < self.j_min:
            tile_j1 = self.j_min
            j1 = 0
        if self.j_max is not None and tile_j2 > self.j_max:
            tile_j2 = self.j_max
            j2 = self.ny - 1

        tile_list = []
        for tj in range(tile_j1, tile_j2 + 1):
            for ti in range(tile_i1, tile_i2 + 1):
                tile_list.append((ti, tj))

        if detail:
            i_beg_dict = {}
            i_end_dict = {}
            i_offset_dict = {}
            j_beg_dict = {}
            j_end_dict = {}
            j_offset_dict = {}

            j_offset = 0
            for tj in range(tile_j1, tile_j2+1):
                j_beg = j1 if tj == tile_j1 else 0
                j_end = j2 + 1 if (tj == tile_j2 and j2 < self.ny) else self.ny
                if margin:
                    j_beg += self.margin
                    j_end += self.margin
                j_size = j_end - j_beg
                j_beg_dict[tj] = j_beg
                j_end_dict[tj] = j_end
                j_offset_dict[tj] = j_offset
                j_offset += j_size
            total_nj = j_offset

            i_offset = 0
            for ti in range(tile_i1, tile_i2+1):
                i_beg = i1 if ti == tile_i1 else 0
                i_end = i2 + 1 if (ti == tile_i2 and i2 < self.nx) else self.nx
                if margin:
                    i_beg += self.margin
                    i_end += self.margin
                i_size = i_end - i_beg
                i_beg_dict[ti] = i_beg
                i_end_dict[ti] = i_end
                i_offset_dict[ti] = i_offset
                i_offset += i_size
            total_ni = i_offset

            x_beg, y_beg = self.tile2xy(tile_i1, tile_j1, i1, j1, margin=False)
            x_end, y_end = self.tile2xy(tile_i2, tile_j2, i2, j2, margin=False)
            total_xs = np.linspace(x_beg, x_end, total_ni)
            total_ys = np.linspace(y_beg, y_end, total_nj)

            return {
                "ni": total_ni,
                "nj": total_nj,
                "xs": total_xs,
                "ys": total_ys,
                "i_beg_dict": i_beg_dict,
                "i_end_dict": i_end_dict,
                "i_offset_dict": i_offset_dict,
                "j_beg_dict": j_beg_dict,
                "j_end_dict": j_end_dict,
                "j_offset_dict": j_offset_dict,
                "tile_list": tile_list
            }
        else:
            return tile_list

    def _to_tile_1d(self, x, orig, block_size, pixel_num):
        x_ = x - orig
        tile_i = int(np.floor(x_ / block_size))
        i = int(np.floor((x_ - block_size * tile_i) / (block_size / pixel_num)))
        if i == pixel_num:
            tile_i += 1
            i = 0
        return tile_i, i

    def _to_xy_1d(self, tile_i, i, orig, block_size, pixel_num, offset=0.5):
        return orig + tile_i * block_size + (i + offset) * block_size / pixel_num

    def get_surrounding_pixels(self, tile_i, tile_j, i, j, length=1, margin=True):
        size = length * 2 + 1
        tile_I = np.full((size, size), tile_i, dtype='i')
        tile_J = np.full((size, size), tile_j, dtype='i')
        J, I = np.mgrid[-length:length+1, -length:length+1]

        if margin:
            i -= self.margin
            j -= self.margin

        J += j
        I += i

        tile_I += I // self.nx
        tile_J += J // self.ny
        I = I % self.nx
        J = J % self.ny

        if margin:
            I += self.margin
            J += self.margin

        return tile_I, tile_J, I, J

    def _parse_ij_lim(self, ij, r):
        mi, ma = (self.i_min, self.i_max) if ij == 'i' else (self.j_min, self.j_max)
        if r is None:
            if mi is None or ma is None:
                raise RuntimeError('Cannot determine ij range')
            else:
                return list(range(mi, ma+1))
        else:
            return list(range(r[0], r[1]+1))

    def merge(self, loader, i_lim=None, j_lim=None):
        """
        Merges data from tiles into a big block
        :param loader: func(tile_i, tile_j) => tile_data
        :param x_lim: None (default) | (i_beg, i_end)
        :param y_lim: None (default) | (j_beg, j_end)
        :param extra_dims: None (default) | (dim tuple)
        :return: data, xs, ys
        """
        i_range = self._parse_ij_lim('i', i_lim)
        j_range = self._parse_ij_lim('j', j_lim)
        total_ny = self.ny * len(j_range)
        total_nx = self.nx * len(i_range)

        data = None
        xs = np.zeros(total_nx, dtype='f8')
        ys = np.zeros(total_ny, dtype='f8')

        for j in j_range:
            j_slice_beg = (j - j_range[0]) * self.ny
            j_slice = slice(j_slice_beg, j_slice_beg + self.ny)
            for i in i_range:
                i_slice_beg = (i - i_range[0]) * self.ny
                i_slice = slice(i_slice_beg, i_slice_beg + self.nx)

                tile_data = loader(i, j)
                if data is None:
                    dtype = tile_data.dtype
                    tile_dims = tile_data.shape
                    total_dims = tile_dims[:-2] + (total_ny, total_nx)
                    data = np.zeros(total_dims, dtype=dtype)

                data[..., j_slice, i_slice] = tile_data

                # Well, this is not efficient, but easier to write.
                tile_xs, tile_ys = self.get_tile_xys(i, j)
                xs[i_slice] = tile_xs
                ys[j_slice] = tile_ys

        return data, xs, ys

    def split(self, data, dumper, i_lim=None, j_lim=None):
        """
        Splits big data block into tiles.
        :param data:
        :param dumper: func(tile_i, tile_j, tile_data, tile_xs, tile_ys)
        :param x_lim: None (default) | (i_beg, i_end)
        :param y_lim: None (default) | (j_beg, j_end)
        :return: None
        """
        i_range = self._parse_ij_lim('i', i_lim)
        j_range = self._parse_ij_lim('j', j_lim)

        for j in j_range:
            j_slice_beg = (j - j_range[0]) * self.ny
            j_slice = slice(j_slice_beg, j_slice_beg + self.ny)
            for i in i_range:
                i_slice_beg = (i - i_range[0]) * self.ny
                i_slice = slice(i_slice_beg, i_slice_beg + self.nx)

                tile_data = data[..., j_slice, i_slice]
                tile_xs, tile_ys = self.get_tile_xys(i, j)
                dumper(i, j, tile_data, tile_xs, tile_ys)

    def __repr__(self):
        return "<{} size: {}, n_pixel: {}, orig: {}, margin: {}>".format(self.__class__.__name__, (self.x_size, self.y_size), (self.nx, self.ny), (self.x0, self.y0), self.margin)