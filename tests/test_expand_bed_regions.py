from ucsc_genomes_downloader import Genome
from ucsc_genomes_downloader.utils import expand_bed_regions
import pytest


def test_expand_bed_regions():
    hg19 = Genome("hg19", chromosomes=["chr2", "chr3"])
    gaps = hg19.gaps(chromosomes=["chr2", "chr3"])
    mask = gaps.chromEnd - gaps.chromStart < 500
    expand_bed_regions(gaps[mask], 1000, "left")
    expand_bed_regions(gaps[mask], 1000, "right")
    expand_bed_regions(gaps[mask], 1000, "center")
    hg19.delete()


def test_expand_bed_regions_wrong_parameters():
    with pytest.raises(ValueError):
        expand_bed_regions(None, -1, "center")
    with pytest.raises(ValueError):
        expand_bed_regions(None, 200, "kebab")
