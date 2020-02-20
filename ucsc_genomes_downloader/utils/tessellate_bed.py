from typing import Tuple
from multiprocessing import Pool, cpu_count
import pandas as pd
from tqdm.auto import tqdm

__all__ = ["tessellate_bed"]


def _tessellate_bed(chrom: str, chromStart: int, chromEnd: int, window_size: int) -> pd.DataFrame:
    """Return tessellated pandas dataframe splitting given window.

    Parameters
    -----------------------
    chrom: str,
        Chromosome containing given window.
    chromStart: int,
        Position where the window starts.
    chromEnd: int,
        Position where the window ends.
    window_size: int
        Target window size.

    Returns
    -----------------------
    Returns a pandas DataFrame in bed-like format containing the tessellated windows.
    """
    return pd.DataFrame([
        {
            "chrom": chrom,
            "chromStart": chromStart + window_size*i,
            "chromEnd": chromStart + window_size*(i+1),
        }
        for i in range((chromEnd - chromStart)//window_size)
    ])


def aligned_tessellate_bed(chrom: str, chromStart: int, chromEnd: int, window_size: int, alignment: str) -> pd.DataFrame:
    """Return tessellated pandas dataframe splitting given window considering given alignment.

    Parameters
    -----------------------
    chrom: str,
        Chromosome containing given window.
    chromStart: int,
        Position where the window starts.
    chromEnd: int,
        Position where the window ends.
    window_size: int,
        Target window size.
    alignment: str,
        Alignment to use for generating windows.
        The alignment can be either "left", "right" or "center".
        Left alignemnt starts from the left of the main window.
        Right alignemnt starts from the right of the main window.
        Center alignemnt removes extra bits from both sides.

    Returns
    -----------------------
    Returns a pandas DataFrame in bed-like format containing the tessellated windows.
    """
    if alignment == "left":
        return _tessellate_bed(
            chrom,
            chromStart,
            chromEnd - chromEnd % window_size,
            window_size
        )
    if alignment == "right":
        return _tessellate_bed(
            chrom,
            chromStart + chromEnd % window_size,
            chromEnd,
            window_size
        )
    return _tessellate_bed(
        chrom,
        chromStart + (chromEnd % window_size)//2,
        chromEnd - (chromEnd % window_size)//2,
        window_size
    )


def _aligned_tessellate_bed(args: Tuple) -> pd.DataFrame:
    return aligned_tessellate_bed(*args)


def tessellate_bed(bed: pd.DataFrame, window_size: int, alignment: str = "left", verbose: bool = True) -> pd.DataFrame:
    """Return tessellated pandas dataframe splitting given window considering given alignment.

    Parameters
    -----------------------
    bed: pd.DataFrame,
        Pandas dataframe in bed-like format.
    window_size: int,
        Target window size.
    alignment: str,
        Alignment to use for generating windows.
        The alignment can be either "left", "right" or "center".
        Left alignemnt starts from the left of the main window.
        Right alignemnt starts from the right of the main window.
        Center alignemnt removes extra bits from both sides.
        Default is left.
    verbose: bool,
        Whetever to show loading bar.
        Default is True.

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

    if alignment not in ("left", "right", "center"):
        raise ValueError((
            "Invalid alignment parameter {alignment}. "
            "Supported values are: left, right or center."
        ).format(alignment=alignment))

    tasks = (
        (row.chrom, row.chromStart, row.chromEnd, window_size, alignment)
        for _, row in bed.iterrows()
    )
    with Pool(cpu_count()) as p:
        df = pd.concat(tqdm(
            p.imap(_aligned_tessellate_bed, tasks),
            total=len(bed),
            disable=not verbose,
            leave=False,
            dynamic_ncols=True,
            desc="Tessellating windows"
        ))
        p.close()
        p.join()
    return df
