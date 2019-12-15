from multiprocessing import Pool, cpu_count
from tqdm.auto import tqdm
import shutil
import os
import json
from roman import toRoman
from typing import List
from .utils import download_tasks, download, merge_genome


def load_all_genomes():
    with open("{pwd}/genomes.json".format(
        pwd=os.path.dirname(os.path.realpath(__file__))
    ), "r") as f:
        return json.load(f)


def load_chromosomes(genome: str):
    genomes = load_all_genomes()
    if genome not in genomes:
        raise ValueError(
            "No default chromosomes were specified for given genome {genome}.".format(
                genome=genome
            )
        )
    chromosomes = genomes[genome]
    numbers = list(range(1, chromosomes["numbers"] + 1))
    if chromosomes["roman_numerals"]:
        numbers = [
            toRoman(n) for n in numbers
        ]
    return [
        "chr{n}".format(n=n) for n in numbers + chromosomes["letters"]
    ]


def download_genome(
        genome: str,
        path: str = ".",
        chromosomes: List[str] = None,
        cache_dir: str = ".genome",
        clear_cache: bool = True,
        clear_compressed_cache: bool = True,
        leave: bool = False,
        merge: bool = True
):
    """Download given genome if it doesn't already exists in given path.
        genome:str,
            The genome to download.
        path:str=".",
            The directory where to save it, by default the current one.
        chromosomes:List[str]=None,
            List of chromosomes to download. By default all those available for given genome.
        cache_dir:str=".genome",
            The directory where to store the download cache.
        clear_cache:bool=True,
            Whetever to clear or now the downloaded chromosomes.
        clear_compressed_cache:bool=True,
            Whetever to clear or now the download cache.
        leave: bool = False,
            Whetever to leave or not the tqdm loading bars. By default, False.
        merge: bool = True,
            Whetever to merge or not the downloaded chromosomes.
    """
    if os.path.exists("{path}/{genome}.fa".format(path=path, genome=genome)):
        return

    if chromosomes is None:
        chromosomes = load_chromosomes(genome)

    tasks = download_tasks(
        genome,
        chromosomes,
        cache_dir,
        clear_compressed_cache
    )
    if tasks:
        with Pool(min(cpu_count(), len(tasks))) as p:
            list(tqdm(
                p.imap(
                    download,
                    tasks
                ),
                total=len(tasks),
                desc="Downloading {genome} chromosomes".format(
                    genome=genome
                ),
                leave=leave
            ))
            p.close()
            p.join()
    if merge:
        merge_genome(path, genome, cache_dir, leave)
    if clear_cache:
        shutil.rmtree(cache_dir)
