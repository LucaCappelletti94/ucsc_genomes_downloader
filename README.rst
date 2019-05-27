UCSC genomes downloader
===================================================================
|travis| |sonar_quality| |sonar_maintainability| |sonar_coverage| |code_climate_maintainability| |pip|

Python package to quickly download genomes from the UCSC.

How do I get this?
----------------------------------------------
As usual, just download it from pip:

.. code:: shell

    pip install ucsc_genomes_downloader

Usage example
---------------------------------------
Suppose you want to download the genome _hg19:

.. code:: python

    from ucsc_genomes_downloader image download_genome
    download_genome("hg19")

There a a couple options, here's a more complete example:

.. code:: python

    from ucsc_genomes_downloader image download_genome
    download_genome(
        genome="hg19",
        path:str=".", # The path where to save the genome, by default the current directory.
        cache_dir:str=".genome", # The path where to store the download cache.
        clear_cache:bool=True # Whetever to delete the download cache, by default True.
    )

.. _hg19: https://www.ncbi.nlm.nih.gov/assembly/GCF_000001405.13/

.. |travis| image:: https://travis-ci.org/LucaCappelletti94/arrp.png
   :target: https://travis-ci.org/LucaCappelletti94/arrp

.. |sonar_quality| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_arrp&metric=alert_status
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_arrp

.. |sonar_maintainability| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_arrp&metric=sqale_rating
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_arrp

.. |sonar_coverage| image:: https://sonarcloud.io/api/project_badges/measure?project=LucaCappelletti94_arrp&metric=coverage
    :target: https://sonarcloud.io/dashboard/index/LucaCappelletti94_arrp

.. |code_climate_maintainability| image:: https://api.codeclimate.com/v1/badges/25fb7c6119e188dbd12c/maintainability
   :target: https://codeclimate.com/github/LucaCappelletti94/arrp/maintainability
   :alt: Maintainability

.. |pip| image:: https://badge.fury.io/py/arrp.svg
    :target: https://badge.fury.io/py/arrp
