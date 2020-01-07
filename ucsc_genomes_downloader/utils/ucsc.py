from requests import get


def get_endpoint(endpoint: str) -> str:
    return "https://api.genome.ucsc.edu/{endpoint}".format(endpoint=endpoint)


def ucsc(endpoint: str):
    return get(get_endpoint(endpoint)).json()


def ucsc_list(endpoint: str):
    return ucsc("list/{endpoint}".format(endpoint=endpoint))


def get_available_genomes():
    return ucsc_list("ucscGenomes")["ucscGenomes"]


def get_available_chromosomes(genome: str):
    return ucsc_list("chromosomes?genome={genome}".format(genome=genome))["chromosomes"]


def get_genome_informations(genome: str):
    return get_available_genomes()[genome]


def chromosome_url(genome: str, chromosome: str, start: int, end: int) -> str:
    return "getData/sequence?genome={genome};chrom={chromosome};start={start};end={end}".format(
        genome=genome,
        chromosome=chromosome,
        start=start,
        end=end
    )


def get_chromosome(genome: str, chromosome: str, start: int, end: int):
    return ucsc(chromosome_url(genome, chromosome, start, end))
