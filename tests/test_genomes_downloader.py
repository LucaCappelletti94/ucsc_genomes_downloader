from ucsc_genomes_downloader import Genome, get_available_genomes
import pytest


def test_create_new_genome_object():
    hg19 = Genome("hg19", clear_cache=True)
    assert len(hg19) == 25
    assert hg19.is_cached()
    hg19 = Genome("hg19")
    hg19.delete()


def test_lazy_download():
    sacCer3 = Genome("sacCer3")
    _ = sacCer3["chrM"]
    sacCer3.delete()


def test_eager_download():
    sacCer3 = Genome("sacCer3", lazy_download=False)
    _ = sacCer3["chrM"]
    sacCer3.delete()


def test_eager_load():
    sacCer3 = Genome("sacCer3", lazy_load=False)
    _ = sacCer3["chrM"]
    sacCer3.delete()


def test_unavailable_genome():
    with pytest.raises(ValueError):
        Genome("hg1")


def test_empty_genome():
    with pytest.raises(ValueError):
        Genome("eboVir3")
