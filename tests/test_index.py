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
    cap_value = int(max_match.group(1))
    assert 1000 <= cap_value <= 10000, "Segment cap should keep per-frame work reasonable"
    assert re.search(
        r"const\s+segments\s*=\s*Math\.min\s*\(\s*clickCount\s*\*\s*80\s*,\s*maxSegments\s*\)",
        content,
        re.S,
    ), "Segments should be capped via Math.min(clickCount * 80, maxSegments)"
    assert re.search(
        r"for\s*\(\s*let\s+([A-Za-z_$][\w$]*)\s*=\s*0\s*;\s*\1\s*<\s*segments\s*;\s*(?:\+\+\1|\1\+\+)\s*\)",
        content,
        re.S,
    ), "Spiral loop should iterate from 0 to segments with a single counter"
