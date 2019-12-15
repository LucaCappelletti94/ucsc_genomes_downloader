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


def test_multiple_downloads():
    genomes = [
        "hg38",
        "hg19",
        "hg18",
        "hg17",
        "hg16",
        "hg15",
        "hg13",
        "hg12",
        "hg11",
        "hg10",
        "mm10",
        "mm9",
        "mm8",
        "mm7",
        "mm6",
        "mm5",
        "mm4",
        "mm3",
        "mm2",
        "mm1"
    ]
    for genome in genomes:
        download_genome(genome, clear_cache=True, chromosomes=["chrM"])
        os.remove(f"{genome}.fa")


def test_invalid_chromosome():
    with pytest.raises(ValueError):
        download_genome("hg19", clear_cache=True, chromosomes=["chrU"])


def test_full_download():
    download_genome("hg19", clear_cache=True)
    assert os.path.exists("hg19.fa")
    os.remove("hg19.fa")
