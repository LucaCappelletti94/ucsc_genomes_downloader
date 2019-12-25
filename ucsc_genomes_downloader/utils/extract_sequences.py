import pandas as pd


def multiprocessing_extract_sequences(kwargs):
    return extract_sequences(**kwargs)


def extract_sequences(bed: pd.DataFrame, sequence: str):
    return pd.DataFrame([
        {
            "chrom": row.chrom,
            "chromStart": row.chromStart,
            "chromEnd": row.chromEnd,
            "sequence": sequence[row.chromStart:row.chromEnd]
        }
        for _, row in bed.iterrows()
    ])
