import os
from bs4 import BeautifulSoup
import re

ROOT = os.path.dirname(os.path.dirname(__file__))
INDEX_PATH = os.path.join(ROOT, "index.html")


def test_assets_exist():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")
    # find all source tags with src attribute
    for tag in soup.find_all(src=True):
        path = os.path.join(ROOT, tag["src"]) 
        assert os.path.exists(path), f"Missing asset: {path}"


def test_spiral_segment_count_is_capped():
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        content = f.read()
    # Ensure a finite cap is applied to the click-influenced segment count
    max_match = re.search(r"const\s+maxSegments\s*=\s*(\d+)", content)
    assert max_match, "Expected a maxSegments constant to bound spiral segments"
    assert int(max_match.group(1)) > 0
    assert "const segments = Math.min(clickCount * 80, maxSegments);" in content
    assert "for(let t=0; t<segments; t++)" in content
