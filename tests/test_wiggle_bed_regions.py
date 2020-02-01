import os
from ucsc_genomes_downloader import Genome
from ucsc_genomes_downloader.utils import wiggle_bed_regions
import pytest
import pandas as pd


def test_tasselize():
    hg19 = Genome("hg19", chromosomes=["chr17"])
    filled = hg19.filled(chromosomes=["chr17"])
    wiggles = wiggle_bed_regions(
        filled,
        max_wiggle_size=100,
        wiggles=10,
        seed=42
    )
    path = "{pwd}/expected_wiggles.csv".format(
        pwd=os.path.dirname(os.path.abspath(__file__))
    )
    if not os.path.exists(path):
        wiggles.to_csv(path, index=False)
    pd.testing.assert_frame_equal(
        wiggles,
        pd.read_csv(path),
        check_dtype=False
    )
    hg19.delete()


def test_tasselize_wrong_parameters():
    with pytest.raises(ValueError):
        wiggle_bed_regions(None, -1, 2, 2)
    with pytest.raises(ValueError):
        wiggle_bed_regions(None, 200, -1, 2)
