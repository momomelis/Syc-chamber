import os
from bs4 import BeautifulSoup

ROOT = os.path.dirname(os.path.dirname(__file__))
INDEX_PATH = os.path.join(ROOT, "index.html")


def test_assets_exist():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    # find all source tags with src attribute
    for tag in soup.find_all(src=True):
        path = os.path.join(ROOT, tag["src"]) 
        assert os.path.exists(path), f"Missing asset: {path}"

