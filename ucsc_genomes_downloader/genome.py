# Copyright (C) 2019 by
#   Luca Cappelletti <luca.cappelletti1@unimi.it>
#
# All rights reserved.
# MIT license.
""" Class to automatically retrieve informations and sequences for a Genome from the UCSC Genome Browser assembly database."""

import json
import os
import shutil
import dateparser
import pandas as pd
import warnings
from math import ceil
from datetime import datetime
from tqdm.auto import tqdm
from multiprocessing import Pool, cpu_count
from typing import Dict, List, Generator
from .utils import get_available_genomes, get_available_chromosomes, get_chromosome, get_genome_informations, is_chromosome_available_online
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

    Downloading lazily a genome
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. code:: python

        from ucsc_genomes_downloader import Genome
        sacCer3 = Genome("sacCer3")
        chrM = sacCer3["chrM"] # Downloads and returns mitochondrial genome

    Downloading eagerly a genome
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. code:: python

        from ucsc_genomes_downloader import Genome
        sacCer3 = Genome("sacCer3", lazy_download=False)

    Loading eagerly a genome
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. code:: python

        from ucsc_genomes_downloader import Genome
        sacCer3 = Genome("sacCer3", lazy_load=False)

    Testing if a genome is cached
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. code:: python

        if hg19.is_cached():
            print("Genome is cached!")

    Removing genome's cache
    ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    .. code:: python

        hg19.delete()


    """

    def __init__(
        self,
        assembly: str,
        unknown_chromosomes: bool = False,
        random_chromosomes: bool = False,
        haplotype_chromosomes: bool = False,
        alternative_chromosomes: bool = False,
        fixed_chromosomes: bool = False,
        mitochondrial_genome: bool = True,
        lazy_load: bool = True,
        lazy_download: bool = True,
        verbose: bool = True,
        leave_loading_bars: bool = False,
        clear_cache: bool = False,
        enable_cache: bool = True,
        warning: bool = True,
        cache_directory: str = None,
        cache_directory_environment_variable: str = "UCSC_GENOMES_CACHE_PATH"
    ):
        """Instantiate a new Genome object.

        Parameters
        ----------
        assembly: str,
            UCSC Genome Browser assembly ID for required genome [1]_.
        unknown_chromosomes: bool = False,
            Whetever to download or not chromosomes containing
            clone contigs that cannot be confidently placed on
            a specific chromosome [1]_.
        random_chromosomes: bool = False,
            Whetever to download or not data related to sequence
            that is known to be in a particular chromosome,
            but could not be reliably ordered within the current sequence [1]_.
        haplotype_chromosomes: bool = False,
            Whetever to download or not data related to sequence
            for alternative haplotypes [1]_.
        alternative_chromosomes: bool = False,
            Whetever to download or not alternative sequences
            that differ from the reference genome currently
            available for a few assemblies including danRer11, hg19, and hg38 [1]_.
        fixed_chromosomes: bool = False,
            Whetever to download or not fix patches currently
            available for the hg19 and hg38 assemblies
            that represent changes to the existing sequence [1]_.
        mitochondrial_genome: bool = True,
            Whetever to download or not the mitocondial genome [2]_.
            A warning is raised if the mitochondrial genome is required
            but none is available for the specified genome.
        lazy_load: bool = True,
            Whetever to lazily load chromosomes as they are required (lazy_load=True) or
            to retrieve them immediately (lazy_load=False).
        lazy_download: bool = True,
            Whetever to lazily download chromosomes as they are required (lazy_download=True) or
            to retrieve them immediately (lazy_download=False). Only available when cache is enabled.
        verbose: bool = True,
            Whetever to show a loading bar when retrieving chromosomes.
        leave_loading_bars: bool = False,
            Whetever to leave or not the loading bars after loading is complete.
        clear_cache: bool = False,
            Whetever to clear cache or not before retrieving chromosomes.
        enable_cache: bool = True,
            Whetever to store data to and load data from given cache directory.
        warning: bool = True,
            Whetever to raise warning when corner cases are detected.
        cache_directory: str = "genomes",
            Position where to store the downloaded genomes.
        cache_directory_environment_variable: str = "UCSC_GENOMES_CACHE_PATH",
            Environment variable where to check if a system-wide directory has
            been specified.

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
        .. [2] https://en.wikipedia.org/wiki/Mitochondrial_DNA
        .. [3] http://hgdownload.soe.ucsc.edu/downloads.html
        """

        self._chromosomes_lenghts = None
        self._genome_informations = None
        self._warning = warning
        self._verbose = verbose
        self._leave_loading_bars = leave_loading_bars
        self._assembly = assembly
        self._enable_cache = enable_cache

        # Checking if a system wide cache directory
        # has been specified
        if cache_directory is None:
                cache_directory = os.environ.get(cache_directory_environment_variable, "genomes")

        self._cache_directory = "{cache_directory}/{assembly}".format(
            cache_directory=cache_directory,
            assembly=self.assembly
        )

        # If required delete cache
        if clear_cache:
            self.delete()

        # If cache is enabled and a directory for the genome
        # exists within the cache we try to load the genome data
        if enable_cache and self.is_cached():
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

        filters = [
            target
            for target, enabled in {
                "chru": unknown_chromosomes,
                "scaffold": unknown_chromosomes,
                "contig": unknown_chromosomes,
                "super": unknown_chromosomes,
                "chrbin": unknown_chromosomes,
                "random": random_chromosomes,
                "hap": haplotype_chromosomes,
                "alt": alternative_chromosomes,
                "fix": fixed_chromosomes,
                "chrm": mitochondrial_genome
            }.items()
            if not enabled
        ]

        # Filtering chromosomes
        self._chromosomes = {
            chromosome: None
            for chromosome in tqdm(
                self._chromosomes_lenghts,
                disable=not verbose,
                leave=leave_loading_bars,
                desc="Filtering chromosomes for the genome {assembly}".format(
                    assembly=self.assembly
                )
            )
            if all(target not in chromosome.lower() for target in filters) and (
                unknown_chromosomes or
                chromosome.lower().startswith("chr")
            ) and self.is_chromosome_available(chromosome)
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

        # If lazy downloading is disabled
        # we immediately proceed to download
        # all the required chromosomes.
        if not lazy_download:
            self.download()

        # If lazy loading is disabled
        # we immediately proceed to load
        # all the required chromosomes.
        if not lazy_load:
            self.load()

    def is_cached(self) -> bool:
        """Return boolean representing if a cache directory already exists for current genome."""
        return os.path.exists(self._cache_directory)

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
            if self._warning:
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
            if self._warning:
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

    def _gaps_path(self) -> str:
        """Return path to default gaps informations."""
        return "{cache_directory}/gaps.bed.gz".format(
            cache_directory=self._cache_directory
        )

    def _load_gaps(self) -> pd.DataFrame:
        """Return a DataFrame with genome gaps."""
        return pd.read_csv(self._gaps_path(), sep="\t")

    def _store_gaps(self, gaps: pd.DataFrame):
        """Store gaps informations into default cache directory."""
        os.makedirs(self._cache_directory, exist_ok=True)
        gaps.to_csv(self._gaps_path(), sep="\t", index=False)

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
        try:
            if self.is_chromosome_cached(chromosome):
                with open(self._chromosome_path(chromosome), "r") as f:
                    return json.load(f)["dna"]
        except Exception:
            if self._warning:
                warnings.warn(
                    "Failed to load chromosome {chromosome} for genome {genome}. "
                    "I will try to download them again afterwards.".format(
                        chromosome=chromosome,
                        genome=self.assembly
                    ),
                    RuntimeWarning
                )
        return None

    def download(self):
        """Download all the genome's chromosomes."""
        chromosomes = [
            chromosome
            for chromosome in self
            if not self.is_chromosome_cached(chromosome)
        ]
        for chromosome in tqdm(
            chromosomes,
            desc="Downloading chromosomes for genome {assembly}".format(
                assembly=self.assembly
            ),
            total=len(chromosomes),
            disable=not self._verbose,
            dynamic_ncols=True,
            leave=self._leave_loading_bars
        ):
            self._download_chromosome(chromosome)

    def delete(self):
        """Remove the genome cache."""
        if os.path.exists(self._cache_directory):
            shutil.rmtree(self._cache_directory)

    def _download_chromosome(self, chromosome: str) -> str:
        """Download and return the nucleotides sequence for the given chromosome.

        Parameters
        ----------
        chromosome: str,
            The chromosome identifier, such as chr1, chrX, chrM...

        Returns
        -------
        The nucleotide sequence for the given chromosomes.
        """
        chromosome_data = get_chromosome(
            self.assembly,
            chromosome,
            0,
            self._chromosomes_lenghts[chromosome]
        )
        if self._enable_cache:
            path = self._chromosome_path(chromosome)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w") as f:
                json.dump(chromosome_data, f)
        return chromosome_data["dna"]

    def load(self):
        """Load into memory all the genome's chromosomes, downloading them when necessary."""
        for chromosome in tqdm(
            self,
            desc="Loading chromosomes for genome {assembly}".format(
                assembly=self.assembly
            ),
            total=len(self),
            disable=not self._verbose,
            dynamic_ncols=True,
            leave=self._leave_loading_bars
        ):
            self[chromosome]

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
        if self._chromosomes[chromosome] is None and self._enable_cache:
            self._chromosomes[chromosome] = self._load_chromosome(
                chromosome
            )
        if self._chromosomes[chromosome] is None:
            self._chromosomes[chromosome] = self._download_chromosome(
                chromosome
            )
        return self._chromosomes[chromosome]

    def items(self) -> Generator:
        """Return generator to iterate through tuples of chromosomes and corresponding sequences."""
        for chromosome in self:
            yield chromosome, self[chromosome]

    def __iter__(self) -> Generator:
        """Return generator to iterate through the genome's chromosomes."""
        for chromosome in self._chromosomes:
            yield chromosome

    def is_chromosome_available(self, chromosome: str) -> bool:
        """Return boolean representing if given chromosome is available either locally or online.

        Parameters
        ----------
        chromosome: str,
            The chromosome identifier, such as chr1, chrX, chrM...

        Returns
        -------
        Boolean representing if given chromosome is available either locally or online.
        """
        return self.is_chromosome_cached(chromosome) or self.is_chromosome_online(chromosome)

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

    def is_chromosome_online(self, chromosome: str) -> bool:
        """Return a boolean representing if given chromosome is available through JSON APIs.

        Parameters
        ----------
        chromosome: str,
            The chromosome identifier, such as chr1, chrX, chrM...

        Raises
        ------
        UserWarning:
            If given chromosome is not available online.

        Returns
        -------
        Boolean representing if given chromosome is available online.
        """
        return is_chromosome_available_online(self.assembly, chromosome)

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

    def gaps(self):
        """Return dataframe in BED format with informations on the gaps.

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
        A DataFrame in BED format.
        """
        if os.path.exists(self._gaps_path()):
            return self._load_gaps()
        with Pool(max(2, min(cpu_count(), len(self)))) as p:
            gaps = pd.concat(list(tqdm(
                p.imap(multiprocessing_gaps, self.items()),
                total=len(self),
                desc="Rendering gaps in {assembly}".format(
                    assembly=self.assembly,
                    leave=self._leave_loading_bars
                ),
                disable=not self._verbose
            )))
            p.close()
            p.join()
        self._store_gaps(gaps)
        return gaps

    def filled(self):
        """Return dataframe with BED-like columns with informations on the gaps."""
        non_gap = []
        gapped_chromosomes = []
        for chrom, values in self.gaps().groupby("chrom"):
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
            } for chrom in self if chrom not in gapped_chromosomes
        ]))
        return pd.concat(non_gap).sort_values(["chrom"]).reset_index(drop=True)

    def bed_to_sequence(self, bed: pd.DataFrame):
        unique_chromosomes = len(bed.chrom.unique())
        tasks = (
            {
                "bed": group,
                "sequence": self[chrom]
            }
            for chrom, group in bed.groupby("chrom")
        )
        with Pool(max(2, min(unique_chromosomes, cpu_count()))) as p:
            sequences = pd.concat(list(tqdm(
                p.imap(
                    multiprocessing_extract_sequences,
                    tasks
                ),
                total=unique_chromosomes,
                desc="Rendering sequences in {assembly}".format(
                    assembly=self.assembly
                ),
                disable=not self._verbose,
                leave=self._leave_loading_bars
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
