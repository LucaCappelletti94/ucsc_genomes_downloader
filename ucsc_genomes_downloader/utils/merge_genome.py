from tqdm.auto import tqdm
import shutil
from glob import glob


def merge_genome(path: str, genome: str, cache_dir: str, leave: bool):
    """Merging the chromosome files into a single genome.

    Parameters
    ----------
    genome:str,
        The genome to download.
    path:str=".",
        The directory where to save it, by default the current one.
    cache_dir:str=".genome",
        The directory where to store the download cache.
    leave: bool,
        Whetever to leave or not the tqdm loading bars.
    """
    with open('{path}/{genome}.fa'.format(path=path, genome=genome), 'wb') as wfd:
        files = glob("{cache_dir}/*.fa".format(cache_dir=cache_dir))
        for f in tqdm(
            files,
            total=len(files),
            desc="Merging genome {genome}".format(genome=genome),
            leave=leave
        ):
            with open(f, 'rb') as fd:
                shutil.copyfileobj(fd, wfd, 1024*1024*10)
