from multiprocessing import Pool, cpu_count
from auto_tqdm import tqdm
import shutil
import os
from typing import List
from .utils import download_tasks, download, merge_genome, all_chromosomes

def download_genome(genome:str, path:str=".", chromosomes:List[str]=None, cache_dir:str=".genome", clear_cache:bool=True):
    """Download given genome if it doesn't already exists in given path.
        genome:str, the genome to download.
        path:str=".", the directory where to save it, by default the current one.
        chromosomes:List[str]=None, list of chromosomes to download. By default all.
        cache_dir:str=".genome", the directory where to store the download cache.
        clear_cache:bool=True, whetever to clear or now the download cache.
    """
    if os.path.exists("{path}/{genome}.fa".format(path=path, genome=genome)):
        return
    chromosomes = all_chromosomes if chromosomes is None else chromosomes
    with Pool(min(cpu_count(), len(chromosomes))) as p:
        list(tqdm(p.imap(download, download_tasks(genome, chromosomes, cache_dir, clear_cache)), total=len(chromosomes), desc="Downloading genome"))
        p.close()
        p.join()
    merge_genome(path, genome, cache_dir)
    if clear_cache:
        shutil.rmtree(cache_dir)
