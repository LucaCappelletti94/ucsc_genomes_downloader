import pandas as pd
import numpy as np


def wiggle_bed_regions(
    bed: pd.DataFrame,
    max_wiggle_size: int,
    wiggles: int,
    seed: int
) -> pd.DataFrame:
    """Return pandas dataframe creating `wiggles` additional examples for each row.

    Parameters
    -----------------------
    bed: pd.DataFrame,
        Pandas dataframe in bed-like format.
    max_wiggle_size: int,
        How much to wiggle the bed regions.
    wiggles: int,
        Number of additional bed regions to generate through wiggling for each row.
    seed: int,
        Random seed to use to reproduce the obtained results.

    Raises
    -----------------------
    ValueError,
        If given max wiggle size is non positive.
    ValueError,
        If given wiggles is non positive.

    Returns
    -----------------------
    Return pandas dataframe creating `wiggles` additional examples for each row.
    """
    if not isinstance(max_wiggle_size, int) or max_wiggle_size < 1:
        raise ValueError("Wiggle size must be a positive integer.")
    if not isinstance(wiggles, int) or wiggles < 1:
        raise ValueError("Wiggles must be a positive integer.")

    # Multiplying rows by given amount
    bed = pd.concat([
        bed
        for _ in range(wiggles)
    ]).reset_index(drop=True)

    # Create random state for reproducibility
    state = np.random.RandomState(seed=seed)
    # Create the wiggles array, with same size of bed file
    # and wiggle from negative max to positive max.
    wiggles = state.randint(-max_wiggle_size, max_wiggle_size, size=len(bed))
    # Apply wiggles
    bed.chromStart += wiggles
    bed.chromEnd += wiggles
    bed.iloc[bed.index[bed.chromStart < 0]].chromStart = 0
    # Return the modified bed file
    return bed
