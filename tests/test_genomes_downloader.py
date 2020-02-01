from ucsc_genomes_downloader import Genome
from ucsc_genomes_downloader.utils import get_available_genomes
import pytest
from glob import glob
import os

sacCer3_chromosomes = ["chrI"]


def test_create_new_genome_object():
    sacCer3 = Genome(
        "sacCer3",
        chromosomes=sacCer3_chromosomes,
    )
    for path in glob("{path}/*.json".format(
        path=sacCer3.path
    )):
        os.remove(path)
    sacCer3 = Genome("sacCer3", chromosomes=sacCer3_chromosomes)
    sacCer3 = Genome("sacCer3", chromosomes=sacCer3_chromosomes)
    sacCer3.gaps()
    sacCer3.filled()
    str(sacCer3)
    sacCer3.delete()


def test_simulated_download_failure():
    for _ in Genome("sacCer3", chromosomes=sacCer3_chromosomes).items():
        pass
    sacCer3 = Genome("sacCer3", chromosomes=sacCer3_chromosomes)
    path = sacCer3._chromosome_path("chrI")
    with open(path, "w") as f:
        f.write("Totally not JSON")
    with pytest.raises(Exception):
        sacCer3 = Genome("sacCer3", chromosomes=sacCer3_chromosomes)
    sacCer3.delete()


def test_get_available_genomes():
    get_available_genomes()


def test_gaps():
    hg19 = Genome("hg19", chromosomes=["chr1"])
    assert "chr1" in hg19
    assert "chr2" not in hg19
    filled = hg19.filled(chromosomes=["chr1"])
    hg19.bed_to_sequence(filled)
    hg19.delete()


def test_unavailable_genome():
    with pytest.raises(ValueError):
        Genome("hg1")


def test_empty_genome():
    with pytest.raises(ValueError):
        Genome("hg19", filters=("",))
