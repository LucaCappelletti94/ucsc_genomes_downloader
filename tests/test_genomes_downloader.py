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
    sacCer3.gaps()
    sacCer3.filled()
    print(sacCer3)
    sacCer3.delete()


def test_simulated_download_failure():
    for _ in Genome("sacCer3").items():
        pass
    sacCer3 = Genome("sacCer3")
    path = sacCer3._chromosome_path("chrM")
    with open(path, "w") as f:
        f.write("Totally not JSON")
    chrM = sacCer3["chrM"]
    assert "chrM" in sacCer3


def test_get_available_genomes():
    get_available_genomes()


def test_gaps():
    hg19 = Genome("hg19")
    filled = hg19.filled(chromosomes=["chr1", "chrM"])
    hg19.bed_to_sequence(filled)
    hg19.delete()


def test_unavailable_genome():
    with pytest.raises(ValueError):
        Genome("hg1")


def test_empty_genome():
    with pytest.raises(ValueError):
        Genome("eboVir3")
