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

Usage example
---------------------------------------
Suppose you want to download the genome _hg19:

.. code:: python

    from ucsc_genomes_downloader image download_genome
    download_genome("hg19")

There are a couple options, here's a more complete example:

.. code:: python

    from ucsc_genomes_downloader image download_genome
    download_genome(
        genome="hg19",
        path=".", # The path where to save the genome, by default the current directory.
        chromosomes=["chr19"], # List of chromosomes to download. By default, all.
        cache_dir=".genome", # The path where to store the download cache.
        clear_cache=True # Whetever to delete the download cache, by default True.
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

.. |pip| image:: https://badge.fury.io/py/ucsc_genomes_downloader.svg
    :target: https://badge.fury.io/py/ucsc_genomes_downloader
    :alt: Pypi project

.. |downloads| image:: https://pepy.tech/badge/ucsc_genomes_downloader
    :target: https://pepy.tech/badge/ucsc_genomes_downloader
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