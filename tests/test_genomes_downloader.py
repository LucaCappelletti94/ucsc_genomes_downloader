from ucsc_genomes_downloader import download_genome
import os
import pytest


def test_genomes_downloader():
    download_genome("hg19", clear_cache=False, chromosomes=["chr19"])
    assert os.path.exists("hg19.fa")
    download_genome("hg19", clear_cache=False, chromosomes=["chr19"])
    assert os.path.exists("hg19.fa")
    os.remove("hg19.fa")
    download_genome("hg19", clear_cache=True, chromosomes=["chr19"])
    assert os.path.exists("hg19.fa")
    os.remove("hg19.fa")


def test_invalid_chromosome():
    with pytest.raises(ValueError):
        download_genome("hg19", clear_cache=True, chromosomes=["chrU"])


def test_full_download():
    download_genome("hg19", clear_cache=True)
    assert os.path.exists("hg19.fa")
    os.remove("hg19.fa")


def test_full_old_download():
    download_genome("hg4", clear_cache=True)
    assert os.path.exists("hg4.fa")
    os.remove("hg4.fa")
