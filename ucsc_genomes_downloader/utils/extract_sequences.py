import pandas as pd


def multiprocessing_extract_sequences(kwargs):
    return extract_sequences(**kwargs)


def extract_sequences(bed: pd.DataFrame, sequence: str) -> pd.DataFrame:
    return pd.DataFrame([
        {
            **row.to_dict(),
            "sequence": sequence[row.chromStart:row.chromEnd]
        }
        for _, row in bed.iterrows()
    ])
