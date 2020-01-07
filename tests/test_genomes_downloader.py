from ucsc_genomes_downloader import Genome, get_available_genomes
import pytest
from glob import glob
import os


def test_create_new_genome_object():
    sacCer3 = Genome(
        "sacCer3",
        clear_cache=True,
        lazy_download=False,
        lazy_load=False
    )
    assert sacCer3.is_cached()
    for path in glob("{path}/*.json".format(
        path=sacCer3.path
    )):
        os.remove(path)
    sacCer3 = Genome("sacCer3")
    sacCer3 = Genome("sacCer3")
    print(sacCer3)
    sacCer3.delete()


def test_get_available_genomes():
    get_available_genomes()


def test_gaps():
    hg19 = Genome("hg19")
    hg19.filled(chromosomes=["chr1", "chrM"])
    hg19.delete()


def test_unavailable_genome():
    with pytest.raises(ValueError):
        Genome("hg1")


def test_empty_genome():
    with pytest.raises(ValueError):
        Genome("eboVir3")
