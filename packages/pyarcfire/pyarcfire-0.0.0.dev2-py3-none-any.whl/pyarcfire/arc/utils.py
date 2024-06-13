from typing import TypeVar

import numpy as np
from numpy.typing import NDArray

FloatType = TypeVar("FloatType", np.float32, np.float64)


def get_polar_coordinates(
    image: NDArray[FloatType],
) -> tuple[NDArray[FloatType], NDArray[FloatType], NDArray[FloatType]]:
    row_indices, column_indices = image.nonzero()
    row_offset = image.shape[0] / 2 - 0.5
    column_offset = image.shape[1] / 2 - 0.5
    x = column_indices - column_offset
    y = -(row_indices - row_offset)

    # Compute polar coordinates and get weights
    radii: NDArray[FloatType] = np.sqrt(np.square(x) + np.square(y))
    theta: NDArray[FloatType] = np.mod(np.arctan2(y, x) + 2 * np.pi, 2 * np.pi)
    weights: NDArray[FloatType] = image[row_indices, column_indices]
    return (radii, theta, weights)


def adjust_theta_to_zero(
    theta: NDArray[FloatType],
    arc_bounds: tuple[float, float],
    offset: float,
    use_modulo: bool,
) -> tuple[NDArray[FloatType], tuple[float, float], float]:
    if use_modulo:
        theta = np.add(np.mod(theta - offset, 2 * np.pi), offset)
    arc_start, _ = arc_bounds
    new_offset = float(offset + arc_start)
    theta += np.subtract(new_offset, np.min(theta))
    arc_bounds = (
        float(arc_bounds[0] - arc_start),
        float(arc_bounds[1] - arc_start),
    )
    return (theta, arc_bounds, new_offset)


def get_arc_bounds(
    offset: float, rotation_amount: float, lower_bound: float, upper_bound: float
) -> tuple[float, float]:
    arc_size = 2 * np.pi - (upper_bound - lower_bound)
    arc_start = np.min(
        (
            __calculate_angle_distance(
                np.array([offset, offset]),
                np.array([lower_bound, upper_bound]),
            )
            + rotation_amount
        )
        % (2 * np.pi)
    )
    return (float(arc_start), float(arc_start) + arc_size)


def __calculate_angle_distance(
    from_angle: NDArray[FloatType], to_angle: NDArray[FloatType]
) -> NDArray[FloatType]:
    is_wrapping = from_angle > to_angle
    distance: NDArray[FloatType] = np.subtract(to_angle, from_angle)
    distance[is_wrapping] += 2 * np.pi
    return distance


def calculate_bounds(
    theta: NDArray[FloatType],
) -> tuple[bool, tuple[float, float], float, float]:
    """Calculates optimisation bounds for the theta offset.
    If the bounds would cross the polar axis, then the bounds must be
    split into two. To avoid this, the theta values can be rotated so that
    the bounds can be expressed as a single bound.

    Parameters
    ----------
    theta : NDArray[FloatType]
        The theta values of the cluster.

    Returns
    -------
    bad_bounds : bool
        This flag is true if the cluster covers a substantial portion
        of the unit circle.
    bounds : tuple[float, float]
        The lower bound and the upper bound of theta offset.
    rotation_amount : float
        The amount to rotate the theta values so that the bounds can be singular.
    max_gap_size : float
        The largest gap between nearby theta values.
    """
    sorted_theta = np.sort(theta)
    gaps = np.diff(sorted_theta)

    end_gap = sorted_theta[0] + 2 * np.pi - sorted_theta[-1]
    max_gap_size = np.max(gaps)
    # If the cluster crosses the polar axis then this is false
    gap_crosses_axis = end_gap > max_gap_size
    # The optimization function lets us restrict theta-offset values by
    # specifying lower and upper bounds.  If the range of allowable
    # values goes through zero, then this range gets split into two
    # parts, which we can't express with a single pair of bounds.  In
    # this case, we temporarily rotate the points to allievate this
    # problem, fit the log-spiral model to the set of rotated points,
    # and then reverse the rotation on the fitted model.
    BAD_BOUNDS_THRESHOLD: float = 0.1
    if not gap_crosses_axis:
        rotation_amount = 0
        max_gap_size_idx = np.argmax(gaps)
        lower_bound = sorted_theta[max_gap_size_idx]
        upper_bound = sorted_theta[max_gap_size_idx + 1]
    else:
        rotation_amount = sorted_theta[0]
        lower_bound = (sorted_theta[-1] - rotation_amount) % (2 * np.pi)
        upper_bound = 2 * np.pi
        max_gap_size = upper_bound - lower_bound
    bounds = (lower_bound, upper_bound)
    bad_bounds = max_gap_size <= BAD_BOUNDS_THRESHOLD
    return (bad_bounds, bounds, rotation_amount, max_gap_size)
