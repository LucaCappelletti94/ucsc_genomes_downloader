from ucsc_genomes_downloader import Genome
from ucsc_genomes_downloader.utils import expand_bed_regions
import pytest
import pandas as pd
pd.options.mode.chained_assignment = "raise" 


def test_expand_bed_regions():
    hg19 = Genome("hg19", chromosomes=["chr2", "chr3"])
    gaps = hg19.gaps(chromosomes=["chr2", "chr3"])
    gaps = gaps[gaps.chromEnd - gaps.chromStart < 500]
    result = expand_bed_regions(gaps, 200, "left")
    assert (result.chromEnd - result.chromStart == 200).all()
    result = expand_bed_regions(gaps, 201, "right")
    assert (result.chromEnd - result.chromStart == 201).all()
    result = expand_bed_regions(gaps, 200, "center")
    assert (result.chromEnd - result.chromStart == 200).all()
    result = expand_bed_regions(gaps, 201, "center")
    assert (result.chromEnd - result.chromStart == 201).all()
    result = expand_bed_regions(gaps, 173, "center")
    assert (result.chromEnd - result.chromStart == 173).all()
    #hg19.delete()


def test_expand_bed_regions_wrong_parameters():
    with pytest.raises(ValueError):
        expand_bed_regions(None, -1, "center")
    with pytest.raises(ValueError):
        expand_bed_regions(None, 200, "kebab")
