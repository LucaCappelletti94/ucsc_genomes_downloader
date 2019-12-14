from tqdm.auto import tqdm
import shutil
from glob import glob


def merge_genome(path: str, genome: str, cache_dir: str):
    """Merging the chromosome files into a single genome.
    genome:str, the genome to download.
    path:str=".", the directory where to save it, by default the current one.
    cache_dir:str=".genome", the directory where to store the download cache.
    """
    with open('{path}/{genome}.fa'.format(path=path, genome=genome), 'wb') as wfd:
        files = glob("{cache_dir}/*.fa".format(cache_dir=cache_dir))
        for f in tqdm(files, total=len(files), desc="Merging genome"):
            with open(f, 'rb') as fd:
                shutil.copyfileobj(fd, wfd, 1024*1024*10)
