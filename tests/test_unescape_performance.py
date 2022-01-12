import logging
import math
import random
from io import StringIO
from typing import Callable, Dict, List, Tuple

import pytest
import enum
from pytest_benchmark.fixture import BenchmarkFixture  # type: ignore[import]

import itertools

from aucampia.rdflib.scratchpad.unquote import unquote


class EscapeGroup(enum.Enum):
    STRING = 1
    NARROW = 3
    WIDE = 4


reserved_escape_chars = r"~.-!$&'()*+,;=/?#@%_"
string_escape_chars = r"""\tbnrf"'"""


lorem_ipsum = """
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam nec malesuada dui. Nunc eu risus semper, porta turpis in, lacinia orci. Phasellus et fringilla elit. Aliquam at purus velit. Etiam turpis eros, bibendum eget lectus sit amet, porttitor pharetra risus. Integer non cursus nunc. Proin tristique placerat nibh, id ornare est lobortis quis. Maecenas eget magna vel nisl viverra hendrerit. Aliquam lacus tellus, posuere eget rhoncus non, mattis in diam. Proin volutpat quam nec finibus tempor. Quisque nisl leo, tempor et sodales ac, sollicitudin sed lacus. Sed nec quam eu elit malesuada suscipit.

Cras mollis enim et molestie rhoncus. Nam eget maximus mi, in mollis tortor. Maecenas et nisi ac dolor euismod auctor. Duis ac ex dictum, lobortis ex quis, egestas nisl. Phasellus imperdiet, lectus sagittis dapibus scelerisque, dolor velit mollis neque, eu malesuada diam neque at tellus. Sed tellus nisl, rhoncus in quam eu, pulvinar fermentum enim. In ut orci ut arcu gravida varius in dapibus erat. Vestibulum efficitur velit in nisi posuere, laoreet molestie ante tempor. Cras ac pulvinar mauris. Vestibulum nec odio vehicula, mattis est vitae, eleifend sem. Ut luctus iaculis fermentum. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae;

In consequat tempor justo quis sollicitudin. Phasellus aliquam erat a justo mollis fringilla sit amet ut purus. Nulla at dui vel ligula porttitor ullamcorper porta eu nibh. Sed imperdiet sem nibh, et maximus nisi tempus dignissim. Integer euismod nisl in lacinia pulvinar. Nulla hendrerit pretium lacus sed tincidunt. Donec vitae neque ac turpis lobortis eleifend. Aliquam semper arcu risus, quis venenatis odio interdum eu. Mauris felis mauris, vehicula sit amet tristique vitae, vehicula eu libero. Duis augue felis, vulputate ac velit sed, mattis condimentum metus. Duis ullamcorper magna nisl, id posuere est ultricies luctus. Quisque a urna ut sapien sodales pellentesque. Phasellus et viverra risus. Aliquam accumsan nisl ligula, vitae dapibus nibh rhoncus a. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec aliquam magna erat, sed euismod nibh dignissim a.

Mauris feugiat justo id tempor ullamcorper. Donec dictum, lectus eu vulputate euismod, arcu sem pharetra sem, ac vulputate elit quam imperdiet turpis. In finibus, tortor sed finibus consequat, ante arcu hendrerit nunc, quis interdum nunc nisi et purus. Phasellus vel odio quis augue varius feugiat. Nulla feugiat nisi id magna condimentum, sed varius elit aliquam. Morbi dapibus, ante eu mollis consequat, arcu ex iaculis dolor, ac vulputate diam nunc vitae est. Suspendisse sit amet elementum dolor. Aenean tempor purus in tincidunt ultricies. Ut ac dui malesuada, tempus libero a, facilisis ex. Curabitur accumsan consectetur lorem non sagittis.

Maecenas vehicula nisl in metus maximus, ut ornare orci consectetur. Sed vel felis ipsum. Sed condimentum, felis quis vulputate malesuada, nisi dui hendrerit sapien, interdum tincidunt lectus mauris at diam. Donec quis orci vel mi viverra rutrum non vitae nisi. Aliquam erat volutpat. Morbi quam lorem, volutpat ut augue id, mattis porttitor felis. Quisque tristique at lectus eu auctor. Aliquam pharetra viverra quam, quis lobortis lorem eleifend sed. Vivamus volutpat ipsum nulla, vel vestibulum lectus luctus nec. Vivamus interdum purus ac felis lacinia, non laoreet sapien commodo. Morbi turpis erat, malesuada vel neque eget, eleifend semper ex. Integer accumsan auctor nisl, nec sagittis orci porttitor dignissim. Interdum et malesuada fames ac ante ipsum primis in faucibus. Proin sit amet eros auctor, ultrices elit eu, suscipit sapien.
""".replace(
    "\n", r" "
)


def add_escapes(
    input: str, escape_groups: List[EscapeGroup], chunk_size: int = 10
) -> str:
    result = StringIO()
    input_len = len(input)
    chunk_count = math.ceil(input_len / chunk_size)
    escape_group_count = len(escape_groups)
    for chunk_index in range(chunk_count):
        chunk = input[(chunk_index + 0) * chunk_size : (chunk_index + 1) * chunk_size]
        # logging.info("chunk == %s", chunk)
        result.write(chunk)
        if escape_group_count == 0:
            continue
        escape_group = escape_groups[chunk_index % escape_group_count]
        if escape_group == EscapeGroup.STRING:
            result.write(f"\\{random.choice('tbnrf')}")
        elif escape_group == EscapeGroup.NARROW:
            chars = "".join(random.choice("123456789abcdefABCDEF") for i in range(4))
            result.write(f"\\u{chars}")
        elif escape_group == EscapeGroup.WIDE:
            chars = "".join(random.choice("123456789abcdefABCDEF") for i in range(4))
            result.write(f"\\U0000{chars}")
    return result.getvalue()


test_strings_map: Dict[str, List[str]] = {
    "no_escapes": [lorem_ipsum],
    "few_escapes": [add_escapes(lorem_ipsum, list(EscapeGroup), 100)],
    "many_escapes": [add_escapes(lorem_ipsum, list(EscapeGroup), 10)],
    "many_escapes_string": [add_escapes(lorem_ipsum, [EscapeGroup.STRING], 10)],
    "many_escapes_narrow": [add_escapes(lorem_ipsum, [EscapeGroup.NARROW], 10)],
    "many_escapes_wide": [add_escapes(lorem_ipsum, [EscapeGroup.WIDE], 10)],
}


def test_add_escapes() -> None:
    assert add_escapes(lorem_ipsum, []) == lorem_ipsum
    logging.info("%s", add_escapes(lorem_ipsum, list(EscapeGroup)))


unescapers: Dict[str, Callable[[str], str]] = {
    "unquote_old": lambda input: unquote(input, validate=False),
    "unquote_validate": lambda input: unquote(input, validate=True),
    "unquote_new": lambda input: unquote(input, new=True),
}


def check_performance(
    unescaper_key: str, test_strings_key: str, benchmark: BenchmarkFixture
) -> None:
    unescaper = unescapers[unescaper_key]
    test_strings = test_strings_map[test_strings_key]

    def unquote_all() -> None:
        for test_string in test_strings:
            unescaper(test_string)

    benchmark(unquote_all)


@pytest.mark.parametrize(
    "unescaper_key, test_strings_key",
    itertools.product(unescapers.keys(), test_strings_map.keys()),
)
def test_performance(
    unescaper_key: str,
    test_strings_key: str,
    benchmark: BenchmarkFixture,
) -> None:
    check_performance(unescaper_key, test_strings_key, benchmark)


# @pytest.mark.parametrize("unescaper_key", unescapers.keys())
# def test_performance_no_escapes(unescaper_key: str, benchmark: BenchmarkFixture) -> None:
#     check_performance(unescaper_key, "no_escapes", benchmark)


# @pytest.mark.parametrize("unescaper_key", unescapers.keys())
# def test_performance_few_escapes(unescaper_key: str, benchmark: BenchmarkFixture) -> None:
#     check_performance(unescaper_key, "few_escapes", benchmark)


# @pytest.mark.parametrize("unescaper_key", unescapers.keys())
# def test_performance_many_escapes(unescaper_key: str, benchmark: BenchmarkFixture) -> None:
#     check_performance(unescaper_key, "many_escapes", benchmark)
