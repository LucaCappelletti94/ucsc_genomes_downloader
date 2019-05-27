from typing import List, Tuple

def format_url(genome:str, chromosome:str)->str:
    """Return formatted download url.
        genome:str, the genome to download.
        chromosome:str, the chromosome to download.
    """
    return "http://hgdownload.cse.ucsc.edu/goldenPath/{genome}/chromosomes/{chromosome}.fa.gz".format(
        genome=genome,
        chromosome=chromosome
    )

def download_tasks(genome:str, chromosomes:List[str], cache_dir:str, clear_cache:bool)->List[Tuple]:
    """Formats the download tasks
        genome:str, genome to download.
        chromosomes:List[str], chromosomes to download.
        cache_dir:str, directory where to store the download cache.
        clear_cache:bool, wheter to delete or not the download cache.
    """
    return [(format_url(genome, c), genome, c, cache_dir, clear_cache) for c in chromosomes]