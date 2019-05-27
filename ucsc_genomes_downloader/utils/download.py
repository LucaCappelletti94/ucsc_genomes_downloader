import requests
import os
from typing import Tuple
from .ungzip import ungzip

def _downloader(url:str, genome:str, chromosome:str, cache_dir:str, clear_cache:bool):
    """Download given chromosome.
        url:str, the url do download.
        genome:str, the genome to download.
        chromosome:str, the chromosome to download.
        cache_dir:str, the directory where to store the download cache.
        clear_cache:bool, whetever to clear or not the download cache.
    """
    path = "{cache_dir}/{genome}".format(genome=genome, cache_dir=cache_dir)
    os.makedirs(path, exist_ok=True)
    file_path = "{path}/{chromosome}.fa.gz".format(path=path, chromosome=chromosome)
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(requests.get(url).content)
    ungzip(file_path)
    if clear_cache:
        os.remove(file_path)


def download(task:Tuple):
    _downloader(*task)