from ucsc_genomes_downloader import download_genome
import os

def test_genomes_downloader():
    download_genome("hg19", clear_cache=False, chromosomes=["chr19"])
    download_genome("hg19", clear_cache=False, chromosomes=["chr19"])
    os.remove("hg19.fa")
    download_genome("hg19", clear_cache=True, chromosomes=["chr19"])
    os.remove("hg19.fa")
