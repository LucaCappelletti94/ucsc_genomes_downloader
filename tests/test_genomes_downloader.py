from ucsc_genomes_downloader import Genome, get_available_genomes
import pytest
from glob import glob
import os


def test_create_new_genome_object():
    sacCer3 = Genome("sacCer3", clear_cache=True)
    assert len(sacCer3) == 25
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
    sacCer3 = Genome("sacCer3")
    chrM = sacCer3["chrM"]
    sacCer3.filled()
    sacCer3.bed_to_sequence(sacCer3.filled().head(1))
    sacCer3.delete()
    hg19 = Genome("hg19")
    hg19.filled()
    hg19.filled()
    hg19.delete()


def test_eagerness():
    sacCer3 = Genome("sacCer3", lazy_download=False)
    path = "{path}/chromosomes/chrM.json".format(
        path=sacCer3.path
    )
    os.remove(path)
    with open(path, "w") as f:
        f.write("Totally not a chromosome")
    sacCer3["chrM"]
    assert "chrM" in sacCer3
    sacCer3.delete()
    sacCer3 = Genome("sacCer3", lazy_load=False)
    sacCer3["chrM"]
    for _ in sacCer3.items():
        pass
    sacCer3.delete()


def test_unavailable_chromosomes():
    with pytest.raises(ValueError):
        Genome("hg1")


def test_empty_genome():
    with pytest.raises(ValueError):
        Genome("eboVir3")
