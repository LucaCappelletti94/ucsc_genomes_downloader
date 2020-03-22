# Copyright (C) 2019 by
#   Luca Cappelletti <luca.cappelletti1@unimi.it>
#
# All rights reserved.
# MIT license.
""" Class to automatically retrieve informations and sequences for a Genome from the UCSC Genome Browser assembly database."""

import json
import os
import math
import shutil
import dateparser
import pandas as pd
import warnings
from datetime import datetime
from tqdm.auto import tqdm
from multiprocessing import Pool, cpu_count
from typing import Dict, Generator, List, Tuple
from .utils import get_available_genomes, get_available_chromosomes, download_chromosome_wrapper, get_genome_informations
from .utils import multiprocessing_gaps, multiprocessing_extract_sequences


class Genome:
    """Class to automatically retrieve informations and sequences for a Genome from the UCSC Genome Browser assembly database.

    Usage examples
    --------------

    Simply instanziate a new genome
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. code:: python

        from ucsc_genomes_downloader import Genome
        hg19 = Genome("hg19")

    Getting gaps regions
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. code:: python

        all_gaps = hg19.gaps() # Returns gaps for all chromosomes
        # Returns gaps for chromosome chrM
        chrM_gaps = hg19.gaps(chromosomes=["chrM"])

    Getting filled regions
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. code:: python

        all_filled = hg19.filled() # Returns filled for all chromosomes
        # Returns filled for chromosome chrM
        chrM_filled = hg19.filled(chromosomes=["chrM"])

    Removing genome's cache
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. code:: python

        hg19.delete()

    """

    def __init__(
        self,
        assembly: str,
        chromosomes: Tuple[str] = None,
        filters: Tuple[str] = ("chru", "chrMT", "scaffold", "contig", "super", "chrbin", "random", "hap", "alt", "fix"),
        verbose: bool = True,
        cache_directory: str = "genomes"
    ):
        """Instantiate a new Genome object.

        Parameters
        ----------
        assembly: str,
            UCSC Genome Browser assembly ID for required genome [1]_.
        chromosomes: Tuple[str] = None,
            Tuple with the chromosomes to download.
            If None (default) all the chromosomes except
            the one filtered out are downloaded.
        filters: Tuple[str] = ("chru", "scaffold", "contig", "super", "chrbin", "random", "hap", "alt", "fix"),
            Tuple containing substring of chromosomes NOT to download.
            If the `chromosomes` parameter is used, no such filter is applied.
        verbose: bool = True,
            Whetever to show a loading bar when retrieving chromosomes.
        cache_directory: str = "genomes",
            Position where to store the downloaded genomes.

        Raises
        ------
        ValueError:
            If the given genome cannot be retrieved either from the given
            cache directory or from the UCSC website [3]_.
        ValueError:
            If the given genome, once the filters have been applied,
            does not contain any chromosome.

        Returns
        -------
        A newly instantiated Genome object.

        References
        ----------
        .. [1] https://genome.ucsc.edu/FAQ/FAQdownloads.html
        """

        self._chromosomes_lenghts = None
        self._genome_informations = None
        self._verbose = verbose
        self._assembly = assembly

        self._cache_directory = os.path.join(cache_directory, self.assembly)

        # If cache is enabled and a directory for the genome
        # exists within the cache we try to load the genome data
        if os.path.exists(self._cache_directory):
            self._genome_informations = self._load_genome_informations()
            self._chromosomes_lenghts = self._load_chromosomes()
        # Otherwise we check if the genome is available
        elif self.assembly not in get_available_genomes():
            # If the genome is not available we raise a proper exception
            raise ValueError(
                "Given genome {assembly} is not within the avalable genomes.".format(
                    assembly=self.assembly
                ))

        # Download genome informations if list is not already loaded
        if self._genome_informations is None:
            self._genome_informations = get_genome_informations(self.assembly)
            # If cache is enabled we store the obtained genome informations
            self._store_genome_informations()

        # Download chromosomes if list is not already loaded
        if self._chromosomes_lenghts is None:
            self._chromosomes_lenghts = get_available_chromosomes(
                self.assembly)
            # If cache is enabled we store the obtained chromosomes lenghts
            self._store_chromosomes()

        # Filtering chromosomes
        self._chromosomes = {
            chrom: None
            for chrom in self._chromosomes_lenghts
            if all(target not in chrom.lower() for target in filters) and chromosomes is None or
            chromosomes is not None and chrom in chromosomes
        }

        # If no chromosome remains after filtering,
        # for instance when the raw data are not yet mapped
        # we raise a userwarning
        if len(self) == 0:
            raise ValueError(
                "No chromosome remaining in chosen genome {assembly}"
                "after executing desired filters"
                "and checking for online availability".format(
                    assembly=self.assembly)
            )

        self._download()
        self._load()

    def _genome_informations_path(self) -> str:
        """Return path for the JSON file with current genome informations."""
        return "{cache_directory}/genome_informations.json".format(
            cache_directory=self._cache_directory
        )

    def _load_genome_informations(self) -> Dict:
        """Return a dictionary with genome informations if available.

        Raises
        ------
        RuntimeWarning:
            If genome informations are not available
            locally.
        """
        try:
            with open(self._genome_informations_path(), "r") as f:
                return json.load(f)
        except Exception:
            warnings.warn(
                "Failed to load genome {genome} informations. "
                "I will try to download them again afterwards.".format(
                    genome=self.assembly
                ),
                RuntimeWarning
            )
        return None

    def _store_genome_informations(self):
        """Store genome informations into default cache directory."""
        os.makedirs(self._cache_directory, exist_ok=True)
        with open(self._genome_informations_path(), "w") as f:
            json.dump(self._genome_informations, f, indent=4)

    def _chromosomes_path(self) -> str:
        """Return path to default chromosomes informations."""
        return "{cache_directory}/chromosomes.json".format(
            cache_directory=self._cache_directory
        )

    def _load_chromosomes(self) -> Dict:
        """Return a dictionary with genome chromosomes if available.

        Raises
        ------
        RuntimeWarning:
            If genome chromosomes are not available
            locally.
        """
        try:
            with open(self._chromosomes_path(), "r") as f:
                return json.load(f)
        except Exception:
            warnings.warn(
                "Failed to load chromosomes for genome {genome}. "
                "I will try to download them again afterwards.".format(
                    genome=self.assembly
                ),
                RuntimeWarning
            )
        return None

    def _store_chromosomes(self):
        """Store chromosomes informations into default cache directory."""
        os.makedirs(self._cache_directory, exist_ok=True)
        with open(self._chromosomes_path(), "w") as f:
            json.dump(self._chromosomes_lenghts, f, indent=4)

    def _chromosome_path(self, chromosome: str) -> str:
        """Return path to the given chromosome.

        Parameters
        ----------
        chromosome: str,
            The chromosome identifier, such as chr1, chrX, chrM...
        """
        return "{cache_directory}/chromosomes/{chromosome}.json".format(
            cache_directory=self._cache_directory,
            chromosome=chromosome
        )

    def _load_chromosome(self, chromosome: str) -> str:
        """Return the nucleotides sequence for the given chromosome.
        Parameters
        ----------
        chromosome: str,
            The chromosome identifier, such as chr1, chrX, chrM...

        Raises
        ------
        RuntimeWarning:
            If given chromosome are not available locally.
        """
        path = self._chromosome_path(chromosome)
        try:
            with open(path, "r") as f:
                return json.load(f)["dna"]
        except json.decoder.JSONDecodeError:
            os.remove(path)
            raise Exception(
                "Chromosome at path {path} is corrupt and has been deleted.".format(path=path))

    def delete(self):
        """Remove the genome cache."""
        if os.path.exists(self._cache_directory):
            shutil.rmtree(self._cache_directory)

    def _download(self):
        """Download the missing chromosomes."""
        tasks = [
            {
                "assembly": self.assembly,
                "chromosome": chromosome,
                "start": 0,
                "end": self._chromosomes_lenghts[chromosome],
                "path": self._chromosome_path(chromosome)
            }
            for chromosome in self
            if not self.is_chromosome_cached(chromosome)
        ]
        if len(tasks):
            with Pool(min(cpu_count(), len(tasks))) as p:
                list(tqdm(
                    p.imap(
                        download_chromosome_wrapper,
                        tasks
                    ),
                    desc="Downloading chromosomes for genome {assembly}".format(
                        assembly=self.assembly
                    ),
                    total=len(tasks),
                    disable=not self._verbose,
                    dynamic_ncols=True,
                    leave=False
                ))
                p.close()
                p.join()

    def _load(self):
        """Load into memory all the genome's chromosomes, downloading them when necessary."""
        for chromosome in tqdm(
            self,
            desc="Loading chromosomes for genome {assembly}".format(
                assembly=self.assembly
            ),
            total=len(self),
            disable=not self._verbose,
            dynamic_ncols=True,
            leave=False
        ):
            self._chromosomes[chromosome] = self._load_chromosome(
                chromosome
            )

    def __len__(self) -> int:
        """Return the number of chromosomes in current genome."""
        return len(self._chromosomes)

    def __contains__(self, chromosome: str) -> bool:
        """Return boolean representing if given chromosome is contained in current genome.

        Parameters
        ----------
        chromosome: str,
            The chromosome identifier, such as chr1, chrX, chrM...

        Returns
        -------
        Boolean representing if given chromosome is contained in current genome.
        """
        return chromosome in self._chromosomes

    def __getitem__(self, chromosome: str):
        """Return sequence data for given chromosome.

        Parameters
        ----------
        chromosome: str,
            The chromosome identifier, such as chr1, chrX, chrM...

        Returns
        -------
        String containing sequence data for given chromosome.
        """
        return self._chromosomes[chromosome]

    def items(self) -> Generator:
        """Return generator to iterate through tuples of chromosomes and corresponding sequences."""
        for chromosome in self:
            yield chromosome, self[chromosome]

    def __iter__(self) -> Generator:
        """Return generator to iterate through the genome's chromosomes."""
        for chromosome in self._chromosomes:
            yield chromosome

    def is_chromosome_cached(self, chromosome: str) -> bool:
        """Return a boolean representing if given chromosome is cached.

        Parameters
        ----------
        chromosome: str,
            The chromosome identifier, such as chr1, chrX, chrM...

        Returns
        -------
        Boolean representing if given chromosome is available locally.
        """
        return os.path.exists(self._chromosome_path(chromosome))

    def __str__(self):
        """Return string representation of current genome."""
        return "{organism}, {scientific_name}, {genome}, {date}, {chromosomes} chromosomes".format(
            organism=self.organism,
            scientific_name=self.scientific_name,
            genome=self.assembly,
            date=self.date,
            chromosomes=len(self)
        )

    __repr__ = __str__

    def gaps(self, chromosomes: List[str] = None):
        """Return dataframe in BED format with informations on the gaps.

        Parameters
        ----------
        chromosomes: List[str] = None,
            List of the chromosomes to parse, by default all.

        FAQs
        ----
        Why don't you just retrieve the gaps from the APIs?
        ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        The gaps track is not always available, therefore for providing a consistent
        usage experience we compute the gaps when required. Additionally, this method
        will work also when you make an offline request, that may sometimes be quite
        useful.

        Returns
        -------
        A DataFrame in BED format containing the gapped regions.
        """
        if chromosomes is None:
            chromosomes = list(self)
        with Pool(min(cpu_count(), len(self))) as p:
            gaps = pd.concat(list(tqdm(
                p.imap(multiprocessing_gaps, (
                    (
                        chromosome, self[chromosome]
                    )
                    for chromosome in chromosomes
                )),
                total=len(chromosomes),
                desc="Rendering gaps in {assembly}".format(
                    assembly=self.assembly
                ),
                leave=False,
                dynamic_ncols=True,
                disable=not self._verbose
            ))).reset_index(drop=True)
            p.close()
            p.join()
        return gaps

    def filled(self,  chromosomes: List[str] = None):
        """Return dataframe with BED-like columns with informations on the gaps.

        Parameters
        ----------
        chromosomes: List[str] = None,
            List of the chromosomes to parse, by default all.

        Returns
        -------
        A DataFrame in BED format containing the filled regions.
        """
        non_gap = []
        gapped_chromosomes = []
        if chromosomes is None:
            chromosomes = list(self)
        for chrom, values in self.gaps(chromosomes).groupby("chrom"):
            # We need to sort by the chromStart
            # as we will need the rows to be ordered
            # to be able to generate the complementary windows
            values = values.sort_values(["chromStart"])
            non_gap_values = pd.DataFrame({
                "chrom": chrom,
                "chromStart": values["chromEnd"][:-1].values,
                "chromEnd": values["chromStart"][1:].values,
            })

            # If the chromosome lenght is not contained
            # within the various chromEnd values it means that
            # the final part of the chromosome is known
            # and therefore considered filled.
            # We need to add this additional row.
            chromosome_lenght = self._chromosomes_lenghts[chrom]
            if values.chromEnd.isin([chromosome_lenght]).any():
                non_gap_values = non_gap_values.append({
                    "chrom": chrom,
                    "chromStart": values.chromEnd.max(),
                    "chromEnd": chromosome_lenght
                }, ignore_index=True)

            # If the chromosome start, the 0 value,
            # is not contained within the various chromStart values
            # it means that the initial part of the chromosome
            # is known and therefore considered filled.
            # We need to add this additional row.
            if values.chromStart.isin([0]).any():
                non_gap_values = non_gap_values.append({
                    "chrom": chrom,
                    "chromStart": 0,
                    "chromEnd": values.chromStart.min(),
                }, ignore_index=True)

            non_gap.append(non_gap_values)
            gapped_chromosomes.append(chrom)

        # When a chromosome does not appear to have
        # any gap is considered fully filled
        non_gap.append(pd.DataFrame([
            {
                "chrom": chrom,
                "chromStart": 0,
                "chromEnd": self._chromosomes_lenghts[chrom]
            } for chrom in chromosomes if chrom not in gapped_chromosomes
        ]))
        return pd.concat(non_gap).sort_values(["chrom"]).reset_index(drop=True)

    def bed_to_sequence(self, bed: pd.DataFrame, chunksize: int = 50000):
        """Return bed with an additional column containing the sequences."""
        tasks = [
            {
                "bed": group[chunksize*i:chunksize*(i+1)],
                "sequence": self[chrom]
            }
            for chrom, group in bed.groupby("chrom")
            for i in range(math.ceil(len(group)/chunksize))
        ]
        with Pool(min(len(tasks), cpu_count())) as p:
            sequences = pd.concat(list(tqdm(
                p.imap(
                    multiprocessing_extract_sequences,
                    tasks
                ),
                total=len(tasks),
                desc="Rendering sequences in {assembly}".format(
                    assembly=self.assembly
                ),
                dynamic_ncols=True,
                disable=not self._verbose,
                leave=False
            )))
            p.close()
            p.join()
        return sequences

    @property
    def assembly(self) -> str:
        """Return genome's UCSC Genome Browser assembly ID."""
        return self._assembly

    @property
    def date(self) -> datetime:
        """Return release date."""
        return dateparser.parse(self.description.split("(")[0]).date()

    @property
    def organism(self) -> str:
        """Return genome's organism."""
        return self._genome_informations["organism"]

    @property
    def scientific_name(self):
        """Return genome's organism scientific name."""
        return self._genome_informations["scientificName"]

    @property
    def description(self):
        """Return genome's description as provided by UCSC."""
        return self._genome_informations["description"]

    @property
    def path(self):
        """Return genome's path."""
        return self._cache_directory
