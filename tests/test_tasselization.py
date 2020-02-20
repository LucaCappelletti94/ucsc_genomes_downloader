from ucsc_genomes_downloader import Genome
from ucsc_genomes_downloader.utils import tessellate_bed
import pytest


def test_tessellate():
    hg19 = Genome("hg19", chromosomes=["chrM"])
    filled = hg19.filled(chromosomes=["chrM"])
    tessellate_bed(filled, window_size=200, alignment="left")
    tessellate_bed(filled, window_size=200, alignment="right")
    tessellate_bed(filled, window_size=200, alignment="center")
    hg19.delete()


def test_tessellate_wrong_parameters():
    with pytest.raises(ValueError):
        tessellate_bed(None, -1, "center")
    with pytest.raises(ValueError):
        tessellate_bed(None, 200, "kebab")
