"""Submodule providing tools to extract and process a genomic sequence."""
from numba import njit, types, typed, prange
from typing import Dict, List
import numpy as np


@njit
def reverse_complement(nucleotides: str, mapping: Dict) -> str:
    """Return reverse complement of given nucletides.

    Parameters
    --------------------------
    nucleotides: str,
        Nucleotides whose reverse complement is to be computed.

    Returns
    --------------------------
    Reverse complement of given nucleotides.
    """
    return "".join([
        mapping[nucleotide]
        for nucleotide in nucleotides
    ])


@njit
def extract_sequence(chromosomes: Dict, chrom: str, chromStart: int, chromEnd: int, strand: str, mapping: Dict) -> str:
    """Return genomic sequence for given coordinates.

    Parameters
    ------------------------------------
    chrom: str,
        Chromosome to use.
    chromStart: int,
        Position from where to start slicing.
    chromEnd: int,
        Position where to stop the slice.

    Returns
    -------------------------------------
    Sequence of nucleotides.
    """
    nucleotides = chromosomes[str(chrom)][chromStart:chromEnd]
    if strand == "-":
        return reverse_complement(nucleotides, mapping)
    return nucleotides


sequence_list_type = types.string


@njit(parallel=True)
def _extract_sequences(
    sequences: List[str],
    chromosomes: Dict,
    chroms: List[str],
    chromStarts: List[int],
    chromEnds: List[int],
    strands: List[str],
    mapping: Dict
):
    """Populates given strings vector."""
    for i in prange(len(chroms)):  # pylint: disable=not-an-iterable
        sequences[i] = extract_sequence(
            chromosomes,
            chroms[i],
            chromStarts[i],
            chromEnds[i],
            str(strands[i]) if strands is not None else str("."),
            mapping
        )


def extract_sequences(
    chromosomes: Dict,
    chroms: List[str],
    chromStarts: List[int],
    chromEnds: List[int],
    strands: List[str],
    mapping: Dict
) -> List[str]:
    maximum_sequence = (chromEnds - chromStarts).max()
    sequences = np.empty(len(chroms), dtype=f"<U{maximum_sequence}")
    _extract_sequences(
        sequences,
        chromosomes,
        chroms,
        chromStarts,
        chromEnds,
        strands,
        mapping,
    )
    return sequences
