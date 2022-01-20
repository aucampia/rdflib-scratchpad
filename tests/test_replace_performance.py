import itertools
import re
from typing import Callable, Dict

import pytest
from pytest_benchmark.fixture import BenchmarkFixture  # type: ignore[import]

PNAME_LOCAL_ESCAPES = re.compile(r"([()])")

replace_method: Dict[str, Callable[[str], str]] = {
    "str_replace": lambda input: input.replace(r"(", r"\(").replace(r")", r"\)"),
    "re_sub": lambda input: PNAME_LOCAL_ESCAPES.sub(r"\\\1", input),
}

test_data = {
    "all": "()" * 10000,
    "none": "abc" * 1000,
}


@pytest.mark.parametrize(
    "method_key, data_key",
    itertools.product(replace_method.keys(), test_data.keys()),
)
def test_translate_performance(
    method_key: str, data_key: str, benchmark: BenchmarkFixture
) -> None:
    method = replace_method[method_key]
    data = test_data[data_key]

    benchmark(lambda: method(data))
