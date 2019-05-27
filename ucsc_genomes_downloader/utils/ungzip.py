import gzip
import shutil

def ungzip(path:str):
    """Ungzip file at given path.
        path:str, path of the file to extract.
    """
    assert path.endswith(".gz")
    with gzip.open(path, 'rb') as f_in:
        with open(path[:-3], 'wb') as f_out:
            shutil.copyfileobj(f_in, f_out)