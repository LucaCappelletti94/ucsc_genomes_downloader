from typing import Dict
from requests import get
import os
import json


def get_endpoint(endpoint: str) -> str:
    return "https://api.genome.ucsc.edu/{endpoint}".format(endpoint=endpoint)


def ucsc(endpoint: str):
    return get(get_endpoint(endpoint)).json()


def ucsc_list(endpoint: str):
    return ucsc("list/{endpoint}".format(endpoint=endpoint))


def get_available_genomes():
    return ucsc_list("ucscGenomes")["ucscGenomes"]


def get_available_chromosomes(genome: str):
    return ucsc_list("chromosomes?genome={genome}".format(genome=genome))["chromosomes"]


def get_genome_informations(genome: str):
    return get_available_genomes()[genome]


def chromosome_url(genome: str, chromosome: str, start: int, end: int) -> str:
    return "getData/sequence?genome={genome};chrom={chromosome};start={start};end={end}".format(
        genome=genome,
        chromosome=chromosome,
        start=start,
        end=end
    )


def get_chromosome(assembly: str, chromosome: str, start: int, end: int):
    return ucsc(chromosome_url(assembly, chromosome, start, end))


def download_chromosome(assembly: str, chromosome: str, start: int, end: int, path: str):
    """Download and return the nucleotides sequence for the given chromosome.

    Parameters
    ----------
    assembly: strm
        The genomic assembly to target.
    chromosome: str,
        The chromosome identifier, such as chr1, chrX, chrM...
    start: int,
        Where to start downloading the chromosome.
    end: int,
        Where to stop downloading the chromosome.
    path: str,
        Where to write the chromosome.

    Returns
    -------
    The nucleotide sequence for the given chromosomes.
    """
    chromosome_data = get_chromosome(assembly, chromosome, start, end)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(chromosome_data, f)


def download_chromosome_wrapper(task: Dict):
    return download_chromosome(**task)
