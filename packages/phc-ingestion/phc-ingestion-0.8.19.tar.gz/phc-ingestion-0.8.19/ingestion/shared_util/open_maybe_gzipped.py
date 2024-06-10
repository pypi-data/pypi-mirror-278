import gzip


def open_maybe_gzipped(filename: str, mode: str = "rt"):
    return gzip.open(filename, mode) if filename.endswith(".gz") else open(filename, mode)
