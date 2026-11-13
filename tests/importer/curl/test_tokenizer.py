
import pytest

from reeeq.importer.curl.tokenizer import split
from .cases import CASES

@pytest.mark.parametrize(
    "case",
    CASES,
    ids=[case["desc"] for case in CASES],
)
def test_tokenizer(case):
    if error := case.get("error"):
        with pytest.raises(error):
            split(case["input"])
    else:
        assert split(case["input"]) == case["expected"]
