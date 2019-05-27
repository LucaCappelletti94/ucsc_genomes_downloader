rm -rf .coverage
coverage erase
pytest -s --cov=ucsc_genomes_downloader --cov-report xml:coverage.xml 
coverage combine 
coverage report
coverage xml