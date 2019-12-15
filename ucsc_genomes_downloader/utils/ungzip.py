import gzip
import os
import zipfile
import shutil


def ungzip(path: str):
    """Ungzip file at given path.
        path:str, path of the file to extract.
    """
    with gzip.open(path, 'rb') as f_in:
        with open(path[:-4], 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)


def unzip(path: str):
    """Unzip file at given path.
        path:str, path of the file to extract.
    """
    with zipfile.ZipFile(path, 'r') as zip_ref:
        zip_ref.extractall("/".join(path.split("/")[:-1]))
    if not os.path.exists(path[:-4]):
        root, chromosome = path[:-4-3].split("chr")
        shutil.move(
            "{root}/{chromosome}/chr{chromosome}.fa".format(
                root=root,
                chromosome=chromosome
            ),
            "{root}/chr{chromosome}.fa".format(
                root=root,
                chromosome=chromosome
            ),
        )
        shutil.rmtree("{root}/{chromosome}".format(
            root=root,
            chromosome=chromosome
        ))
