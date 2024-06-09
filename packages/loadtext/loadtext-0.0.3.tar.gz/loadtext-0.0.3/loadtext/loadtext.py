"""
Load text with best effort to determine encoding.

Based on en-de-zh-txt\load_text.py
"""
from typing import List, Union
from pathlib import Path
import re

# import cchardet
# from logzero import logger
import charset_normalizer
from loguru import logger


def loadtext(filename: Union[str, Path], splitlines: bool = True) -> Union[str, List[str]]:
    """Load text for given filepath.

    Args
    ----
    filename (str|Path): filename
    splitlines (bool): output list of pars if True, defaul True

    Returns
    ---
    text with blank lines removed or list or pars
    """
    if not Path(filename).is_file():
        _ = Path(filename).resolve().as_posix()

        # raise SystemExit(f"{_} does not exist or is not a file")
        # better to raise an Exception
        raise Exception(f"{_} does not exist or is not a file")
    try:
        _ = charset_normalizer.detect(Path(filename).read_bytes())
    except Exception as exc:  # pylint: disable=broad-except
        logger.warning(f"charset_normalizer exc: {exc}, setting encoding to utf8")
        _ = {"encoding": "utf8"}
    encoding = _["encoding"]

    try:
        cont = Path(filename).read_text(encoding)
    except Exception as exc:
        logger.error(f"read_text exc: {exc}")
        raise

    # replace unicode spaces with normal space " "
    cont = re.sub(r"[\u3000]", " ", cont)

    _ = [elm.strip() for elm in cont.splitlines() if elm.strip()]

    # list of paragraphs with blank lines removed
    if splitlines:
        return _

    # text with blank lines removed
    return "\n".join(_)
