import numpy as np


def space(start, stop, power_slope, size):
    """
    Parameters
    ----------
    start : float
        Lower limit of the space.
    stop : float
        Upper limit of the space.
    power_slope : float
        Slope of the power law.
    size : int
        The number of samples.

    Returns
    -------
    x : array_like
        Values between 'start' and 'stop' spaced to histogram a power law
        with slope 'power_slope' in equal amounts in each bin.
    """
    # Adopted from CORSIKA
    rd = np.linspace(0.0, 1.0, size)
    if power_slope != -1.0:
        ll = start ** (power_slope + 1.0)
        ul = stop ** (power_slope + 1.0)
        slex = 1.0 / (power_slope + 1.0)
        return (rd * ul + (1.0 - rd) * ll) ** slex
    else:
        ll = stop / start
        return start * ll**rd


def spacing(start, stop, x, power_slope):
    """
    Parameters
    ----------
    start : float
        Start of the bin
    stop : float
        Stop of the bin
    x : float
        Value
    power_slope : float
        Slope of the power law.

    Returns
    -------
    pos : float
        The position where x has to be put in the linear interval from start to
        stop.
    """
    if power_slope != -1.0:
        inv_slex = power_slope + 1.0
        p_x = x**inv_slex
        p_start = start**inv_slex
        p_stop = stop**inv_slex
        return (p_x - p_start) / (p_stop - p_start)
    else:
        return np.log(x / start) / np.log(stop / start)


def query_ball(bin_edges, start, stop, power_slope):
    """
    Parameters
    ----------
    bin_edges : array_like, floats
        Edges of bins with power spacing according to power_slope.
    start : float
        Start of the range/ball to query.
    stop : float
        Stop of the range/ball to query.
    power_slope : float
        The spectral index used in the power space used to create bin_edges.

    Returns
    -------
    (bins, weights) : (array_like ints, array_like floats)
        The indices and weights of the bins touching the queried range/ball.
    """
    num_bins = len(bin_edges) - 1
    assert num_bins >= 1
    assert stop >= start

    bins = []
    weights = []
    for b in range(num_bins):
        bin_start = bin_edges[b]
        bin_stop = bin_edges[b + 1]

        if start < bin_start:
            start_sector = 0
        elif start >= bin_start and start < bin_stop:
            start_sector = 1
        else:
            start_sector = 2

        if stop < bin_start:
            stop_sector = 0
        elif stop >= bin_start and stop < bin_stop:
            stop_sector = 1
        else:
            stop_sector = 2

        # | overlap |               sectors
        # |         |     0      |     1      |     2
        # | ------- | ------------------------------------
        # |         | start stop |            |
        # |  True   | start      | stop       |
        # |  True   | start      |            |       stop
        # |  True   |            | start stop |
        # |  True   |            | start      |       stop
        # |         |            |            | start stop

        if start_sector == 0:
            if stop_sector == 1:
                oo = spacing(
                    start=bin_start,
                    stop=bin_stop,
                    x=stop,
                    power_slope=power_slope,
                )
                if oo > 0.0:
                    bins.append(b)
                    weights.append(oo)
            if stop_sector == 2:
                bins.append(b)
                weights.append(1.0)
        if start_sector == 1:
            if stop_sector == 1:
                ostart = spacing(
                    start=bin_start,
                    stop=bin_stop,
                    x=start,
                    power_slope=power_slope,
                )
                ostop = spacing(
                    start=bin_start,
                    stop=bin_stop,
                    x=stop,
                    power_slope=power_slope,
                )
                oo = ostop - ostart
                bins.append(b)
                weights.append(oo)
            if stop_sector == 2:
                ostart = spacing(
                    start=bin_start,
                    stop=bin_stop,
                    x=start,
                    power_slope=power_slope,
                )
                oo = 1.0 - ostart
                bins.append(b)
                weights.append(oo)

    return np.array(bins), np.array(weights)
