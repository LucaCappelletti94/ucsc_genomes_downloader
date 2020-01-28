ucsc_genomes_downloader
=========================================================================================
|travis| |sonar_quality| |sonar_maintainability| |codacy|
|code_climate_maintainability| |pip| |downloads|

Python package to quickly download and work with genomes from the UCSC.

How do I install this package?
----------------------------------------------
As usual, just download it using pip:

.. code:: shell

    pip install ucsc_genomes_downloader

Tests Coverage
----------------------------------------------
Since some software handling coverages sometime get
slightly different results, here's three of them:

|coveralls| |sonar_coverage| |code_climate_coverage|

Usage examples
--------------

Simply instanziate a new genome
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from ucsc_genomes_downloader import Genome
    hg19 = Genome("hg19")

Downloading selected chromosomes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    from ucsc_genomes_downloader import Genome
    hg19 = Genome("hg19", chromosomes=["chr1", "chr2"])

Getting gaps regions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The method return a DataFrame in bed-like format
that contains the regions where only n or N nucleotides
are present.

.. code:: python

    all_gaps = hg19.gaps() # Returns gaps (region formed of Ns) for all chromosomes
    # Returns gaps for chromosome chrM
    chrM_gaps = hg19.gaps(chromosomes=["chrM"])

Getting filled regions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
The method return a DataFrame in bed-like format
that contains the regions where no unknown
nucleotide is present, basically the complementary
of the gaps method.

.. code:: python

    all_filled = hg19.filled() # Returns filled for all chromosomes
    # Returns filled for chromosome chrM
    chrM_filled = hg19.filled(chromosomes=["chrM"])

Removing genome's cache
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    hg19.delete()

Utilities
-------------------------------

Retrieving a list of the available genomes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You can get a complete list of the genomes available
from the UCSC website with the following method:

.. code:: python

    from ucsc_genomes_downloader.utils import get_available_genomes
    all_genomes = get_available_genomes()


Tasselizing bed files
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Create a tasselization of a given size of a given bed-like pandas dataframe.

Available alignment are to the left, right or center.

.. code:: python

    from ucsc_genomes_downloader.utils import tasselize_bed
    import pandas as pd

    my_bed = pd.read_csv("path/to/my/file.bed", sep="\t")
    tasselized = tasselize_bed(
        my_bed,
        window_size=200,
        alignment="left"
    )

Expand bed files regions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Expand a given dataframe in bed-like format using selected alignment.

Available alignment are to the left, right or center.

.. code:: python

    from ucsc_genomes_downloader.utils import expand_bed_regions
    import pandas as pd

    my_bed = pd.read_csv("path/to/my/file.bed", sep="\t")
    expanded = expand_bed_regions(
        my_bed,
        window_size=1000,
        alignment="left"
    )

.. _hg19: https://www.ncbi.nlm.nih.gov/assembly/GCF_000001405.13/

.. |travis| image:: https://travis-ci.org/LucaCappelletti94/ucsc_genomes_downloader.png
   :target: https://travis-ci.org/LucaCappelletti94/ucsc_genomes_downloader
   :alt: Travis CI build

.. |sonar_quality| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_ucsc_genomes_downloader&metric=alert_status
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_ucsc_genomes_downloader
    :alt: SonarCloud Quality

.. |sonar_maintainability| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_ucsc_genomes_downloader&metric=sqale_rating
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_ucsc_genomes_downloader
    :alt: SonarCloud Maintainability

.. |sonar_coverage| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_ucsc_genomes_downloader&metric=coverage
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_ucsc_genomes_downloader
    :alt: SonarCloud Coverage

.. |coveralls| image:: https://coveralls.io/repos/github/LucaCappelletti94/ucsc_genomes_downloader/badge.svg?branch=master
    :target: https://coveralls.io/github/LucaCappelletti94/ucsc_genomes_downloader?branch=master
    :alt: Coveralls Coverage

.. |pip| image:: https://badge.fury.io/py/ucsc-genomes-downloader.svg
    :target: https://badge.fury.io/py/ucsc-genomes-downloader
    :alt: Pypi project

.. |downloads| image:: https://pepy.tech/badge/ucsc-genomes-downloader
    :target: https://pepy.tech/badge/ucsc-genomes-downloader
    :alt: Pypi total project downloads

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/79564bf70059458b8a9ee6e775f4c7d2
    :target: https://www.codacy.com/app/LucaCappelletti94/ucsc_genomes_downloader?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=LucaCappelletti94/ucsc_genomes_downloader&amp;utm_campaign=Badge_Grade
    :alt: Codacy Maintainability

.. |code_climate_maintainability| image:: https://api.codeclimate.com/v1/badges/9cd5ed4d4e41892ccc9d/maintainability
    :target: https://codeclimate.com/github/LucaCappelletti94/ucsc_genomes_downloader/maintainability
    :alt: Maintainability

.. |code_climate_coverage| image:: https://api.codeclimate.com/v1/badges/9cd5ed4d4e41892ccc9d/test_coverage
    :target: https://codeclimate.com/github/LucaCappelletti94/ucsc_genomes_downloader/test_coverage
    :alt: Code Climate Coverate
