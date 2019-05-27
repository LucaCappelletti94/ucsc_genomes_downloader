from auto_tqdm import tqdm
import shutil
from glob import glob

def merge_genome(path: str, genome: str, cache_dir:str):
    with open('{path}/{genome}.fa'.format(path=path, genome=genome), 'wb') as wfd:
        for f in tqdm(glob("{cache_dir}/{genome}/*.fa".format(cache_dir=cache_dir, genome=genome)), total=24, desc="Merging genome"):
            with open(f, 'rb') as fd:
                shutil.copyfileobj(fd, wfd, 1024*1024*10)