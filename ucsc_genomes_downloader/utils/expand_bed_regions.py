import pandas as pd
import numpy as np

__all__ = ["expand_bed_regions"]


def expand_bed_regions(bed: pd.DataFrame, window_size: int, alignment: str = "center") -> pd.DataFrame:
    """Return pandas dataframe setting regions to given window size considering given alignment.

    Parameters
    -----------------------
    bed: pd.DataFrame,
        Pandas dataframe in bed-like format.
    window_size: int,
        Target window size.
    alignment: str,
        Alignment to use for generating windows.
        The alignment can be either "left", "right" or "center".
        Left alignemnt expands on the right, keeping the left position fixed.
        Right alignemnt expands on the left, keeping the right position fixed.
        Center alignemnt expands on both size equally, keeping the center position fixed.
        Default is center.

    Comments
    -----------------------
    For enhancers peaks usually one should generally use center alignment,
    while when working on promoters peaks either right or left alignment
    should be used depending on the strand, respectively for positive (right)
    and negative (left) strand.

    Raises
    -----------------------
    ValueError,
        If given window size is non positive.
    ValueError,
        When given alignment is not supported.

    Returns
    -----------------------
    Returns a pandas DataFrame in bed-like format containing the tessellated windows.
    """
    if not isinstance(window_size, int) or window_size < 1:
        raise ValueError("Window size must be a positive integer.")

    if alignment == "left":
        bed.chromEnd = bed.chromStart + window_size
    elif alignment == "right":
        bed.chromStart = bed.chromEnd - window_size
    elif alignment == "center":
        mid_point = (bed.chromEnd + bed.chromStart)//2
        bed.chromStart = (mid_point - np.floor(window_size/2)).astype(int)
        bed.chromEnd = (mid_point + np.ceil(window_size/2)).astype(int)
    else:
        raise ValueError((
            "Invalid alignment parameter {alignment}. "
            "Supported values are: left, right or center."
        ).format(alignment=alignment))
    return bed
