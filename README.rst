ucsc_genomes_downloader
=========================================================================================
|travis| |sonar_quality| |sonar_maintainability| |codacy| |code_climate_maintainability| |pip| |downloads|

Python package to quickly download genomes from the UCSC.

How do I install this package?
----------------------------------------------
As usual, just download it using pip:

.. code:: shell

    pip install ucsc_genomes_downloader

Tests Coverage
----------------------------------------------
Since some software handling coverages sometime get slightly different results, here's three of them:

|coveralls| |sonar_coverage| |code_climate_coverage|

Usage examples
--------------

Simply instanziate a new genome
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Create a new `Genome` object for the given genome hg19.

.. code:: python

    from ucsc_genomes_downloader import Genome
    hg19 = Genome("hg19")

Downloading lazily a genome's chromosome
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Download mitochondrial genome "chromosome" for the genome "sacCer3" (downloads the chromosomes only when required).

.. code:: python

    from ucsc_genomes_downloader import Genome
    sacCer3 = Genome("sacCer3")
    chrM = sacCer3["chrM"] # Downloads and returns mitochondrial genome

Downloading eagerly a genome
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Download all genome's chromosomes immediately.

.. code:: python

    from ucsc_genomes_downloader import Genome
    sacCer3 = Genome("sacCer3", lazy_download=False)

Loading eagerly a genome
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Load (and downloads if necessary) into RAM all the genome's chromosomes immediately.

.. code:: python

    from ucsc_genomes_downloader import Genome
    sacCer3 = Genome("sacCer3", lazy_load=False)

Testing if a genome is cached
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    if hg19.is_cached():
        print("Genome is cached!")

Getting gaps regions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    all_gaps = hg19.gaps() # Returns gaps for all chromosomes
    chrM_gaps = hg19.gaps(chromosomes=["chrM"]) # Returns gaps for chromosome chrM

Getting filled regions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    all_filled = hg19.filled() # Returns filled for all chromosomes
    chrM_filled = hg19.filled(chromosomes=["chrM"]) # Returns filled for chromosome chrM

Removing genome's cache
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    hg19.delete()

Utilities
-------------------------------

Retrieving a list of the available genomes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
You can get a complete list of the genomes available from the UCSC website with the following method:

.. code:: python

    from ucsc_genomes_downloader import get_available_genomes
    all_genomes = get_available_genomes()

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

.. |codacy|  image:: https://api.codacy.com/project/badge/Grade/79564bf70059458b8a9ee6e775f4c7d2
    :target: https://www.codacy.com/app/LucaCappelletti94/ucsc_genomes_downloader?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=LucaCappelletti94/ucsc_genomes_downloader&amp;utm_campaign=Badge_Grade
    :alt: Codacy Maintainability

.. |code_climate_maintainability| image:: https://api.codeclimate.com/v1/badges/9cd5ed4d4e41892ccc9d/maintainability
    :target: https://codeclimate.com/github/LucaCappelletti94/ucsc_genomes_downloader/maintainability
    :alt: Maintainability

.. |code_climate_coverage| image:: https://api.codeclimate.com/v1/badges/9cd5ed4d4e41892ccc9d/test_coverage
    :target: https://codeclimate.com/github/LucaCappelletti94/ucsc_genomes_downloader/test_coverage
    :alt: Code Climate Coverate
