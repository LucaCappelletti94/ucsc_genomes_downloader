from ucsc_genomes_downloader import Genome, get_available_genomes


def test_create_new_genome_object():
    hg19 = Genome("hg19")
    assert len(hg19) == 25
    assert hg19.is_cached()
    hg19.delete()


def test_lazy_download():
    sacCer3 = Genome("sacCer3")
    _ = sacCer3["chrM"]
    sacCer3.delete()


def test_eager_download():
    sacCer3 = Genome("sacCer3", lazy_download=False)
    _ = sacCer3["chrM"]
    sacCer3.delete()


def test_eager_load():
    sacCer3 = Genome("sacCer3", lazy_load=False)
    _ = sacCer3["chrM"]
    sacCer3.delete()
