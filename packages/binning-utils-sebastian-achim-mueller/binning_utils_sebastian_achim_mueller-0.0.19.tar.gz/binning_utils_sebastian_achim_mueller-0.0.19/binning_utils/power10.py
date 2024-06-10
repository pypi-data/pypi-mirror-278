"""
A binning that has its edges aligned with the decade.
Choose how many bins you want within a decade and query the edges of the bins.
"""
import numpy as np


def lower_bin_edge(decade, bin, num_bins_per_decade=5):
    """
    Returns the lower edge of bin in decade.
    The binning has num_bins_per_decade.

    Parameters
    ----------
    decade : int
        E.g. decade=0 is 10^{0} = 1.0
    bin : int
        Index of bin within decade.
    num_bins_per_decade : int
        A decade has this many bins.

    Returns
    -------
    lower edge of bin : float
    """
    assert num_bins_per_decade > 0
    assert 0 <= bin < num_bins_per_decade
    return 10 ** (decade + (bin / num_bins_per_decade))


def make_decade_and_bin_combinations(
    start_decade, start_bin, stop_decade, stop_bin, num_bins_per_decade=5
):
    """
    Computes input-parameters to lower_bin_edge() in a given range.

    Parameters
    ----------
    start_decade : int
    start_bin : int
    stop_decade : int
    stop_bin : int
    num_bins_per_decade : int

    Returns
    -------
    A list of input-parameters to lower_bin_edge().
    """
    combos = []

    assert 0 <= stop_bin < num_bins_per_decade
    assert 0 <= start_bin < num_bins_per_decade
    assert start_decade <= stop_decade

    d = start_decade
    b = start_bin
    while decade_bin_is_less((d, b), (stop_decade, stop_bin)):
        combos.append((d, b))
        d, b = decade_bin_increase(d, b, num_bins_per_decade)
    return combos


def space(
    start_decade, start_bin, stop_decade, stop_bin, num_bins_per_decade=5
):
    """
    Power10.space:
    Compute the bin-edges starting from: (start_decade, start_bin)
    up to: (stop_decade, stop_bin).

    Parameters
    ----------
    start_decade : int
    start_bin : int
    stop_decade : int
    stop_bin : int
    num_bins_per_decade : int

    Returns
    -------
    Edges of bins : array of floats
    """
    combis = make_decade_and_bin_combinations(
        start_decade=start_decade,
        start_bin=start_bin,
        stop_decade=stop_decade,
        stop_bin=stop_bin,
        num_bins_per_decade=num_bins_per_decade,
    )
    out = np.nan * np.ones(len(combis))
    for i, combi in enumerate(combis):
        out[i] = lower_bin_edge(
            decade=combi[0],
            bin=combi[1],
            num_bins_per_decade=num_bins_per_decade,
        )
    return out


def find_upper_decade_and_bin(x, num_bins_per_decade=5):
    """
    Returns the bin's upper edge (decade, bin) to include value x.
    """
    decade = int(np.log10(x))
    bin_factor = lower_bin_edge(
        decade=0,
        bin=1,
        num_bins_per_decade=num_bins_per_decade,
    )
    xn = float(x / (10**decade))
    b = 0
    while b < num_bins_per_decade:
        xn = xn / bin_factor
        b += 1
        if xn < 1.0:
            return decade, b
    return decade, b


def find_lower_decade_and_bin(x, num_bins_per_decade=5):
    """
    Returns the bin's lower edge (decade, bin) to include value x.
    """
    upper = find_upper_decade_and_bin(
        x=x, num_bins_per_decade=num_bins_per_decade
    )
    return decade_bin_decrease(
        decade=upper[0], bin=upper[1], num_bins_per_decade=num_bins_per_decade
    )


def decade_bin_increase(decade, bin, num_bins_per_decade):
    """
    Returns the next higher bin-edge's (decade, bin).
    """
    if bin == num_bins_per_decade - 1:
        return decade + 1, 0
    else:
        return decade, bin + 1


def decade_bin_decrease(decade, bin, num_bins_per_decade):
    """
    Returns the next lower bin-edge's (decade, bin).
    """
    if bin == 0:
        return decade - 1, num_bins_per_decade - 1
    else:
        return decade, bin - 1


def decade_bin_is_less(dec_bin_A, dec_bin_B):
    decA = dec_bin_A[0]
    decB = dec_bin_B[0]
    binA = dec_bin_A[1]
    binB = dec_bin_B[1]
    if decA < decB:
        return True
    elif decA == decB:
        return binA < binB
    else:
        return False
