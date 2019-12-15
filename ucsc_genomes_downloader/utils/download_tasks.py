from typing import List, Tuple
import requests


def format_url(genome: str, chromosome: str) -> str:
    """Return formatted download url.
        genome:str, the genome to download.
        chromosome:str, the chromosome to download.
    """
    candidate_extensions = ("gz", "zip")
    for candidate_extension in candidate_extensions:
        candidate_url = "http://hgdownload.cse.ucsc.edu/goldenPath/{genome}/chromosomes/{chromosome}.fa.{candidate_extension}".format(
            genome=genome,
            chromosome=chromosome,
            candidate_extension=candidate_extension
        )
        if requests.head(candidate_url).status_code == 200:
            return candidate_url
    raise ValueError(
        "No file has been found searching for extensions {candidate_extensions} for genome {genome} and chromosome {chromosome}".format(
            candidate_extensions=", ".join(candidate_extensions),
            genome=genome,
            chromosome=chromosome
        )
    )


def download_tasks(genome: str, chromosomes: List[str], cache_dir: str, clear_cache: bool) -> List[Tuple]:
    """Formats the download tasks
        genome:str, genome to download.
        chromosomes:List[str], chromosomes to download.
        cache_dir:str, directory where to store the download cache.
        clear_cache:bool, wheter to delete or not the download cache.
    """
    return [(format_url(genome, c), c, cache_dir, clear_cache) for c in chromosomes]
