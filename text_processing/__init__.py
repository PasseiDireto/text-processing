import os
import pathlib
import shutil

import nlpnet
import nltk
import requests
from tqdm import tqdm

local_dir = os.path.dirname(__file__)


def download(url, filepath):
    with requests.get(url, stream=True) as response:
        response.raise_for_status()
        with open(filepath, "wb") as f:
            pbar = tqdm(total=int(response.headers["Content-Length"]))
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
                    pbar.update(len(chunk))


# Download pos-pt ----------------------

pos_dir = os.path.join(local_dir, "pos")
pos_pt = os.path.join(pos_dir, "pos-pt")

if not os.path.exists(pos_pt):

    if not os.path.exists(pos_dir):
        os.makedirs(pos_dir)

    print("Downloading pos-pt...")
    url = "http://nilc.icmc.usp.br/nlpnet/data/pos-pt.tgz"
    download(url, f"{pos_pt}.tgz")

    shutil.unpack_archive(f"{pos_pt}.tgz", os.path.realpath(pos_dir))

    if os.path.isfile(f"{pos_pt}.tgz"):
        pathlib.Path(f"{pos_pt}.tgz").unlink()

# Download nltk data -------------------

nltk_dir = os.path.join(local_dir, "nltk_data")
tokn_dir = os.path.join(nltk_dir, "tokenizers")

nltk.data.path += [nltk_dir]

try:
    nltk.data.find(os.path.join("tokenizers", "punkt", "portuguese.pickle"))

except LookupError:

    if not os.path.exists(tokn_dir):
        os.makedirs(tokn_dir)

    punkt = os.path.join(tokn_dir, "punkt.zip")

    print("Downloading nltk data...")
    url = "https://raw.githubusercontent.com/nltk/nltk_data/gh-pages/packages/tokenizers/punkt.zip"
    download(url, punkt)

    shutil.unpack_archive(punkt, os.path.realpath(tokn_dir))

    if os.path.isfile(punkt):
        pathlib.Path(punkt).unlink()

nlpnet.set_data_dir(pos_pt)

from ._processing import *
from ._tagging import getKeywords
