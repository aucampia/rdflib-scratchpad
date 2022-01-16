import logging
import math
import random
from io import StringIO
from this import d
from typing import Callable, Dict, List, Tuple

import pytest
import enum
from pytest_benchmark.fixture import BenchmarkFixture  # type: ignore[import]


import itertools

from aucampia.rdflib.scratchpad.unquote import (
    decodeUnicodeEscape,
    unquote,
    _string_escape_map,
    _string_escape_translator,
)

translate_methods: Dict[str, Callable[[str], str]] = {
    "dt": lambda input: _string_escape_map[input],
    "tr": lambda input: input.translate(_string_escape_translator),
}

test_data = "".join(_string_escape_map.keys()) * 10000


@pytest.mark.parametrize(
    "translate_method_key",
    translate_methods.keys(),
)
def test_translate_performance(
    translate_method_key: str, benchmark: BenchmarkFixture
) -> None:
    translate_method = translate_methods[translate_method_key]

    def translate_all() -> None:
        for chr in test_data:
            translate_method(chr)

    benchmark(translate_all)
