from ucsc_genomes_downloader import Genome
from ucsc_genomes_downloader.utils import tasselize_bed
import pytest


def test_tasselize():
    hg19 = Genome("hg19", chromosomes=["chrM"])
    filled = hg19.filled(chromosomes=["chrM"])
    tasselize_bed(filled, window_size=200, alignment="left")
    tasselize_bed(filled, window_size=200, alignment="right")
    tasselize_bed(filled, window_size=200, alignment="center")
    hg19.delete()


def test_tasselize_wrong_parameters():
    with pytest.raises(ValueError):
        tasselize_bed(None, -1, "center")
    with pytest.raises(ValueError):
        tasselize_bed(None, 200, "kebab")
