import requests
import os
from typing import Tuple
from .ungzip import ungzip, unzip


def _downloader(
    url: str,
    chromosome: str,
    cache_dir: str,
    clear_compressed_cache: bool
):
    """Download given chromosome.
        url:str, the url do download.
        chromosome:str, the chromosome to download.
        cache_dir:str, the directory where to store the download cache.
        clear_compressed_cache:bool, whetever to clear or not the download cache.
    """
    os.makedirs(cache_dir, exist_ok=True)
    file_path = "{cache_dir}/{chromosome}.fa.tmp".format(
        cache_dir=cache_dir,
        chromosome=chromosome
    )
    target_path = file_path[:-4]
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(requests.get(url).content)
    if url.endswith(".gz"):
        ungzip(file_path)
    elif url.endswith(".zip"):
        unzip(file_path)
    else:
        ValueError("Unknown compression extension for file at url {url}".format(
            file_path=file_path
        ))
    if clear_compressed_cache:
        os.remove(file_path)


def download(task: Tuple):
    _downloader(*task)
