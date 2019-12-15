from ucsc_genomes_downloader import download_genome
from ucsc_genomes_downloader.download_genome import load_chromosomes, load_all_genomes
import os
import json
import pytest
from tqdm.auto import tqdm
import random


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
    for genome in tqdm(load_all_genomes(), "Genomes"):
        download_genome(
            genome,
            chromosomes=random.choice(load_chromosomes(genome)),
            clear_cache=True
        )
        os.remove(f"{genome}.fa")


def test_invalid_chromosome():
    with pytest.raises(ValueError):
        download_genome("hg19", clear_cache=True, chromosomes=["chrU"])
