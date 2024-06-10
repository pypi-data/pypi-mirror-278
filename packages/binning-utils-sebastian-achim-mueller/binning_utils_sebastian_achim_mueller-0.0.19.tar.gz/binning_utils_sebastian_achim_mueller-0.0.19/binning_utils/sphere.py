import numpy as np


def fibonacci_space(size=1000, max_zenith_distance_rad=np.pi):
    """
    Fibonacci-sphere/space
    ----------------------
    Returns the coordinates of points on a sphere which form a reasonable
    tiling where the tiles are similar in solid angle and shape.
    Of course it is not a perfect tiling (can not be) but it gets close enough
    to be useful for practical means.

    Parameters
    ----------
    size : int
        Number of points on the sphere.
    max_zenith_distance_rad : float
        Maximum zenith-distance (zenith is pos. z-axis) to put points.
        Default is Pi, what is the full sphere.

    Inspired by 'Fnord'.
    """
    points = []
    phi = np.pi * (np.sqrt(5.0) - 1.0)  # golden angle in radians

    z_start = 1
    z_stop = np.cos(max_zenith_distance_rad)

    for i, z in enumerate(np.linspace(z_start, z_stop, size)):
        radius = np.sqrt(1 - z * z)  # radius at z

        theta = phi * i  # golden angle increment

        x = np.cos(theta) * radius
        y = np.sin(theta) * radius

        points.append([x, y, z])

    return np.array(points)
