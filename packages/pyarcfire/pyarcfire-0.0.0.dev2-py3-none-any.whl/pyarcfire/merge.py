"""This module contains functions relating to calculating merging errors."""

import logging
import numpy as np
from numpy.typing import NDArray

from .arc import fit_spiral_to_image

log: logging.Logger = logging.getLogger(__name__)

FloatType = np.float32


def calculate_arc_merge_error(
    first_cluster_array: NDArray[FloatType], second_cluster_array: NDArray[FloatType]
) -> float:
    """Calculates the arc merge error ratio for two clusters. This is a measure of how
    well the merged cluster of the two clusters given fit to a log spiral compared to
    fitting the two clusters separately.

    Parameters
    ----------
    first_cluster_array : Array2D
        The first cluster in the form of an array.
    second_cluster_array : Array2D
        The second cluster in the form of an array.

    Returns
    -------
    merge_error_ratio : float
        The arc merge error ratio.
    """

    first_sum = first_cluster_array.sum()
    second_sum = second_cluster_array.sum()
    # Verify we don't have division by zero or weird negative weights
    if first_sum <= 0 or second_sum <= 0:
        raise ValueError("The cluster arrays must sum to a positive value.")
    total_sum = first_sum + second_sum
    # Adjust weights
    first_cluster_array *= total_sum / first_sum
    second_cluster_array *= total_sum / second_sum

    # Fit spirals to each cluster individually
    first_fit = fit_spiral_to_image(first_cluster_array)
    second_fit = fit_spiral_to_image(second_cluster_array)

    combined_cluster_array = first_cluster_array + second_cluster_array
    # Fit a spiral to both clusters at the same time
    first_merged_fit = fit_spiral_to_image(
        combined_cluster_array,
        initial_pitch_angle=first_fit.pitch_angle,
    )
    second_merged_fit = fit_spiral_to_image(
        combined_cluster_array,
        initial_pitch_angle=second_fit.pitch_angle,
    )
    if first_merged_fit.total_error <= second_merged_fit.total_error:
        merged_fit = first_merged_fit
    else:
        merged_fit = second_merged_fit

    first_cluster_indices = (first_cluster_array > 0)[combined_cluster_array > 0]
    # Get the error of the merged spiral for each individual cluster
    first_cluster_errors = merged_fit.errors[first_cluster_indices].sum()
    second_cluster_errors = merged_fit.errors[~first_cluster_indices].sum()

    # Readjust errors from normalised cluster arrays
    first_cluster_error_weighted = first_fit.total_error / first_sum
    second_cluster_error_weighted = second_fit.total_error / second_sum

    # Calculate the arc merge error ratio for each cluster
    ratios = (
        ((first_cluster_errors / first_sum) / first_cluster_error_weighted),
        ((second_cluster_errors / second_sum) / second_cluster_error_weighted),
    )
    # Return the worst error ratio
    return max(ratios)
