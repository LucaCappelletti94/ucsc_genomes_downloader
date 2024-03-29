UCSC Genomes Downloader
=========================================================================================
|python_version| |pip| |downloads|

Python package to quickly download and process genomes from the UCSC website.

How do I install this package?
----------------------------------------------
As usual, just download it using pip:

.. code:: shell

    pip install ucsc_genomes_downloader
    
Getting COVID-19 Genome
----------------------------------------------
To download the COVID19 genome just run:

.. code:: python

    from ucsc_genomes_downloader import Genome
    covid = Genome("wuhCor1")
    
    genome = covid["NC_045512v2"]


Usage examples
--------------

Simply instantiate a new genome
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To download and load into memory the chromosomes of a given genomic assembly
you can use the following code snippet:

.. code:: python

    from ucsc_genomes_downloader import Genome
    hg19 = Genome(assembly="hg19")

Downloading selected chromosomes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you want to select a subset of chromosomes to be downloaded
you can use the attribute "chromosomes":

.. code:: python

    from ucsc_genomes_downloader import Genome
    hg19 = Genome("hg19", chromosomes=["chr1", "chr2"])

Getting gaps regions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The method returns a DataFrame in bed-like format
that contains the regions where only n or N nucleotides
are present.

.. code:: python

    all_gaps = hg19.gaps() # Returns gaps (region formed of Ns) for all chromosomes
    # Returns gaps for chromosome chrM
    chrM_gaps = hg19.gaps(chromosomes=["chrM"])

Getting filled regions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The method returns a DataFrame in bed-like format
that contains the regions where no unknown nucleotides
are present, basically the complementary
of the gaps method.

.. code:: python

    all_filled = hg19.filled() # Returns filled for all chromosomes
    # Returns filled for chromosome chrM
    chrM_filled = hg19.filled(chromosomes=["chrM"])

Removing genome's cache
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
To delete the cache of the genome, including chromosomes
and metadata you can use the delete method:

.. code:: python

    hg19.delete()

Genome objects representation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
When printed, a Genome object has a human-readable representation.
This allows you to print lists of Genome objects as follows:

.. code:: python

    print([
        hg19,
        hg38,
        mm10
    ])

    # >>> [
    #    Human, Homo sapiens, hg19, 2009-02-28, 25 chromosomes,
    #    Human, Homo sapiens, hg38, 2013-12-29, 25 chromosomes,
    #    Mouse, Mus musculus, mm10, 2011-12-29, 22 chromosomes
    # ]

Obtaining a given bed file sequences
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Given a pandas DataFrame in bed-like format, you can obtain
the corresponding genomic sequences for the loaded assembly
using the bed_to_sequence method:

.. code:: python

    my_bed = pd.read_csv("path/to/my/file.bed", sep="\t")
    sequences = hg19.bed_to_sequence(my_bed)

Properties
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A Genome object has the following properties:

.. code:: python

    hg19.assembly # Returns "hg19"
    hg19.date # Returns "2009-02-28" as datetime object
    hg19.organism # Returns "Human"
    hg19.scientific_name # Returns "Homo sapiens"
    hg19.description # Returns the brief description as provided from UCSC
    hg19.path # Returns path where genome is cached


Utilities
-------------------------------

Retrieving a list of the available genomes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You can get a complete list of the genomes available
from the UCSC website with the following method:

.. code:: python

    from ucsc_genomes_downloader.utils import get_available_genomes
    all_genomes = get_available_genomes()


Tessellating bed files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Create a tessellation of a given size of a given bed-like pandas dataframe.

Available alignments are to the left, right or center.

.. code:: python

    from ucsc_genomes_downloader.utils import tessellate_bed
    import pandas as pd

    my_bed = pd.read_csv("path/to/my/file.bed", sep="\t")
    tessellated = tessellate_bed(
        my_bed,
        window_size=200,
        alignment="left"
    )

Expand bed files regions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Expand a given dataframe in bed-like format using selected alignment.

Available alignments are to the left, right or center.

.. code:: python

    from ucsc_genomes_downloader.utils import expand_bed_regions
    import pandas as pd

    my_bed = pd.read_csv("path/to/my/file.bed", sep="\t")
    expanded = expand_bed_regions(
        my_bed,
        window_size=1000,
        alignment="left"
    )

Wiggle bed files regions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Generate new bed regions based on a given bed file by wiggling the
initial regions.

.. code:: python

    from ucsc_genomes_downloader.utils import wiggle_bed_regions
    import pandas as pd

    my_bed = pd.read_csv("path/to/my/file.bed", sep="\t")
    expanded = wiggle_bed_regions(
        my_bed,
        max_wiggle_size=100, # Maximum amount to wiggle region
        wiggles=10, # Number of wiggled samples to introduce
        seed=42 # Random seed for reproducibility
    )

.. _hg19: https://www.ncbi.nlm.nih.gov/assembly/GCF_000001405.13/

.. |pip| image:: https://badge.fury.io/py/ucsc-genomes-downloader.svg
    :target: https://badge.fury.io/py/ucsc-genomes-downloader
    :alt: Pypi project

.. |downloads| image:: https://pepy.tech/badge/ucsc-genomes-downloader
    :target: https://pepy.tech/badge/ucsc-genomes-downloader
    :alt: Pypi total project downloads

.. |python_version| image:: https://img.shields.io/badge/python-3.x-blue
    :alt: Supported Python Versions