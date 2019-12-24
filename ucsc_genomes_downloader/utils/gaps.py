import pandas as pd
from typing import Tuple


def multiprocessing_gaps(task: Tuple[str, str]):
    return gaps(*task)


def gaps(chrom: str, sequence: str):
    i = 0
    chromStart = None
    chunksize = 500
    max_chunk_size = 10000
    # We iterate through chunks of given size
    lower = sequence.lower()
    sequence_lenght = len(sequence)
    regions = pd.DataFrame(columns=[
        "chrom",
        "chromStart",
        "chromEnd"
    ])
    while i < sequence_lenght:
        chunk = lower[i:i+chunksize]
        # If all characters of the line respect the region rule
        # we can just proceed on after having, if not already done
        # marked the chromStart. Then we update the counter.
        if {"n"}.issuperset(chunk):
            if chromStart is None:
                chromStart = i
            i += len(chunk)
            if chunksize < max_chunk_size:
                chunksize *= 2
            continue
        # If not a single character of the line respects the region rule
        # we can just proceed on directly after having closed the previous region
        # if one was already open.
        if "n" not in chunk:
            if chromStart is not None:
                regions = regions.append({
                    "chrom": chrom,
                    "chromStart": chromStart,
                    "chromEnd": i
                }, ignore_index=True)
                chromStart = None
            i += len(chunk)
            if chunksize < max_chunk_size:
                chunksize *= 2
            continue
        # If at least a character within the line respectes the region rule
        # we need to parse the chunk, nucleotide by nucleotide.
        chunksize = 100
        for nucleotide in chunk:
            is_unknown = nucleotide == "n"
            if is_unknown and chromStart is None:
                chromStart = i
            elif not is_unknown and chromStart is not None:
                regions = regions.append({
                    "chrom": chrom,
                    "chromStart": chromStart,
                    "chromEnd": i
                }, ignore_index=True)
                chromStart = None
            i += 1
    if chromStart is not None:
        regions = regions.append({
            "chrom": chrom,
            "chromStart": chromStart,
            "chromEnd": i,
        }, ignore_index=True)
    return regions
