"""
=======================================
Contour plot of irregularly spaced data
=======================================

Comparison of a contour plot of irregularly spaced data interpolated
on a regular grid versus a tricontour plot for an unstructured triangular grid.

Since `~.axes.Axes.contour` and `~.axes.Axes.contourf` expect the data to live
on a regular grid, plotting a contour plot of irregularly spaced data requires
different methods. The two options are:

* Interpolate the data to a regular grid first. This can be done with on-board
  means, e.g. via `~.tri.LinearTriInterpolator` or using external functionality
  e.g. via `scipy.interpolate.griddata`. Then plot the interpolated data with
  the usual `~.axes.Axes.contour`.
* Directly use `~.axes.Axes.tricontour` or `~.axes.Axes.tricontourf` which will
  perform a triangulation internally.

This example shows both methods in action.
"""
# https://matplotlib.org/stable/gallery/images_contours_and_fields/irregulardatagrid.html#sphx-glr-gallery-images-contours-and-fields-irregulardatagrid-py

import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np


def create_regular_xyz():
    np.random.seed(19680801)
    npts: int = 200
    ngridx: int = 100
    ngridy: int = 200
    x = np.random.uniform(-2, 2, npts)
    y = np.random.uniform(-2, 2, npts)
    z = x * np.exp(-x**2 - y**2)
    return x, y, z, ngridx, ngridy, npts


def create_map(x, y, z, ngridx, ngridy, npts, num):
    if num == 2:
        fig, (ax1, ax2) = plt.subplots(nrows=2)

        # -----------------------
        # Interpolation on a grid
        # -----------------------
        # A contour plot of irregularly spaced data coordinates
        # via interpolation on a grid.

        # Create grid values first.
        xi = np.linspace(-2.1, 2.1, ngridx)
        yi = np.linspace(-2.1, 2.1, ngridy)

        # Linearly interpolate the data (x, y) on a grid defined by (xi, yi).
        triang = tri.Triangulation(x, y)
        interpolator = tri.LinearTriInterpolator(triang, z)
        Xi, Yi = np.meshgrid(xi, yi)
        print(Xi)
        print(Yi)
        zi = interpolator(Xi, Yi)

        # Note that scipy.interpolate provides means to interpolate data on a grid
        # as well. The following would be an alternative to the four lines above:
        # from scipy.interpolate import griddata
        # zi = griddata((x, y), z, (xi[None, :], yi[:, None]), method='linear')

        ax1.contour(xi, yi, zi, levels=14, linewidths=0.5, colors='k')
        cntr1 = ax1.contourf(xi, yi, zi, levels=14, cmap="RdBu_r")

        fig.colorbar(cntr1, ax=ax1)
        ax1.plot(x, y, 'ko', ms=3)
        ax1.set(xlim=(-2, 2), ylim=(-2, 2))
        ax1.set_title('grid and contour (%d points, %d grid points)' %
                      (npts, ngridx * ngridy))
    else:
        fig, ax2 = plt.subplots(nrows=1)

# ----------
# Tricontour
# ----------
# Directly supply the unordered, irregularly spaced coordinates
# to tricontour.
    xp=[0.1, 3.5, 4.9, 6.2, 7, 9, 9, 9, 9, 6.5, 4.5, 2.9, 1.3, 0,
    0, 0, 1.7, 2.2, 2.5, 2.9, 3.2, 1.6, 4.7, 4.6, 4.5, 4.6, 4.5, 4.3, 4.4, 5.3, 6,
    6.9, 7.1, 7, 6.9, 6.9, 7, 6, 6, 5.9, 6, 6.3, 3, 4, 5, 0.6, 1.8]
    x11 = np.array(xp)
    # print(len(x11))
    yp = [0, 0, 0, 0, 0, 0, 5, 3, 7, 7, 7, 7, 7, 7, 4.1, 2.1, 5.6, 4.5,
    3.6, 2.4, 1.1, 6.6, 1, 1.6, 2.5, 3.6, 4.2, 5.1, 6, 5.3, 5.7, 5.6, 5, 3.5, 2.7,
    1.9, 0.6, 1, 2, 3, 4, 4.8, 6, 4.5, 4.5, 5, 2]
    y11 = np.array(yp)
    # print(len(y11))
    zp = [90, 45, 65, 40, 55, 25, 55, 48, 45, 75, 50, 75, 52, 70, 90,
    105, 75, 66, 60, 55, 50, 60, 66, 70, 80, 95, 80, 70, 60, 78, 88, 102, 104,
    90, 80, 70, 60, 51, 54, 60, 64, 71, 75, 75, 73, 80, 70]
    z11 = np.array(zp)
    # print(len(z11))

    ax2.tricontour(x11, y11, z11, levels=14, linewidths=0.5, colors='k')
    cntr2 = ax2.tricontourf(x11, y11, z11, levels=14, cmap="RdBu_r")

    fig.colorbar(cntr2, ax=ax2)
    ax2.plot(x11, y11, 'ko', ms=3)
    ax2.set(xlim=(min(x11), max(x11)), ylim=(min(y11), max(y11)))
    ax2.set_title('tricontour')

    plt.subplots_adjust(hspace=1)
    plt.show()

def create_single_map(x: np.ndarray, y: np.ndarray, z: np.ndarray, map_title: str):
    fig, ax2 = plt.subplots(nrows=1)
    ax2.tricontour(x, y, z, levels=14, linewidths=0.5, colors='k')
    cntr2 = ax2.tricontourf(x, y, z, levels=14, cmap="RdBu_r")

    fig.colorbar(cntr2, ax=ax2)
    ax2.plot(x, y, 'ko', ms=3)
    ax2.set(xlim=(min(x), max(x)), ylim=(min(y), max(y)))
    ax2.set_title('map_title')

    plt.subplots_adjust(hspace=1)
    plt.show()

def create_srf_dat() -> (np.ndarray, np.ndarray, np.ndarray):
    xp=[0.1, 3.5, 4.9, 6.2, 7, 9, 9, 9, 9, 6.5, 4.5, 2.9, 1.3, 0,
    0, 0, 1.7, 2.2, 2.5, 2.9, 3.2, 1.6, 4.7, 4.6, 4.5, 4.6, 4.5, 4.3, 4.4, 5.3, 6,
    6.9, 7.1, 7, 6.9, 6.9, 7, 6, 6, 5.9, 6, 6.3, 3, 4, 5, 0.6, 1.8]
    x11 = np.array(xp)
    print(len(x11))
    print(type(x11))
    print(x11.dtype)
    yp = [0, 0, 0, 0, 0, 0, 5, 3, 7, 7, 7, 7, 7, 7, 4.1, 2.1, 5.6, 4.5,
    3.6, 2.4, 1.1, 6.6, 1, 1.6, 2.5, 3.6, 4.2, 5.1, 6, 5.3, 5.7, 5.6, 5, 3.5, 2.7,
    1.9, 0.6, 1, 2, 3, 4, 4.8, 6, 4.5, 4.5, 5, 2]
    y11 = np.array(yp)
    print(len(y11))
    print(type(y11))
    print(y11.dtype)
    zp = [90, 45, 65, 40, 55, 25, 55, 48, 45, 75, 50, 75, 52, 70, 90,
    105, 75, 66, 60, 55, 50, 60, 66, 70, 80, 95, 80, 70, 60, 78, 88, 102, 104,
    90, 80, 70, 60, 51, 54, 60, 64, 71, 75, 75, 73, 80, 70]
    z11 = np.array(zp)
    # print(len(z11))
    return x11, y11, z11


def test_irregular():
    (x, y, z, ngridx, ngridy, npts) = create_regular_xyz()
    create_map(x, y, z, ngridx, ngridy, npts, num = 1)

def test_srf_map():
    (x, y, z) = create_srf_dat()
    create_single_map(x, y, z, map_title='title')

# test_irregular()
test_srf_map()
#############################################################################
#
# ------------
#
# References
# """"""""""
#
# The use of the following functions and methods is shown in this example:

# import matplotlib
# matplotlib.axes.Axes.contour
# matplotlib.pyplot.contour
# matplotlib.axes.Axes.contourf
# matplotlib.pyplot.contourf
# matplotlib.axes.Axes.tricontour
# matplotlib.pyplot.tricontour
# matplotlib.axes.Axes.tricontourf
# matplotlib.pyplot.tricontourf
