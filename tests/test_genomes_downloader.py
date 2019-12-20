from ucsc_genomes_downloader import Genome, get_available_genomes
import pytest
from glob import glob
import os


def test_create_new_genome_object():
    hg19 = Genome("hg19", clear_cache=True)
    assert len(hg19) == 25
    assert hg19.is_cached()
    for path in glob("{path}/*.json".format(
        path=hg19.path
    )):
        os.remove(path)
    hg19 = Genome("hg19")
    hg19 = Genome("hg19")
    hg19.delete()


def test_lazy_download():
    sacCer3 = Genome("sacCer3")
    _ = sacCer3["chrM"]
    _ = sacCer3["chrM"]
    sacCer3.delete()


def test_eagerness():
    sacCer3 = Genome("sacCer3", lazy_download=False)
    path = "{path}/chromosomes/chrM.json".format(
        path=sacCer3.path
    )
    os.remove(path)
    with open(path, "w") as f:
        f.write("Totally not a chromosome")
    _ = sacCer3["chrM"]
    assert "chrM" in sacCer3
    sacCer3.delete()
    sacCer3 = Genome("sacCer3", lazy_load=False)
    _ = sacCer3["chrM"]
    for _ in sacCer3.items():
        pass
    sacCer3.delete()


def test_unavailable_genome():
    with pytest.raises(ValueError):
        Genome("hg1")


def test_empty_genome():
    with pytest.raises(ValueError):
        Genome("eboVir3")
