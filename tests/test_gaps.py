from ucsc_genomes_downloader import Genome
import pandas as pd

def test_gaps():
    hg19 = Genome("hg19", chromosomes=["chr1"])
    assert "chr1" in hg19
    assert "chr2" not in hg19
    # Check that no gap is with 0 length
    gaps = hg19.gaps(["chr1"])
    assert (gaps.chromEnd - gaps.chromStart != 0).all()
    # Converting gaps to sequences: should all be Nns
    gaps_sequences = hg19.bed_to_sequence(gaps)
    for gap in gaps_sequences:
        assert set(gap.lower()) == set(["n"])
    filled = hg19.filled(["chr1"])
    assert (filled.chromEnd - filled.chromStart != 0).all()
    filled_sequences = hg19.bed_to_sequence(filled)
    for fl in filled_sequences:
        assert "n" not in fl.lower()
    hg19.delete()
