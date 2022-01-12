import logging
import math
import random
from io import StringIO
from typing import Callable, Dict, List, Tuple

import pytest
import enum
from pytest_benchmark.fixture import BenchmarkFixture  # type: ignore[import]


import itertools

from aucampia.rdflib.scratchpad.unquote import (
    decodeUnicodeEscape,
    unquote,
    _string_escape_map,
)


class EscapeGroup(enum.Enum):
    RESERVED = 0
    STRING = 1
    UNICODE = 2
    NARROW = 3
    WIDE = 4


reserved_escape_chars = r"~.-!$&'()*+,;=/?#@%_"
string_escape_chars = r"""\tbnrf"'"""


def make_test_data() -> List[Tuple[str, str]]:
    result = []

    def add_pair(escape: str, unescaped: str) -> None:
        result.append((f"\\{escape}", unescaped))
        result.append((f"\\\\{escape}", f"\\{escape}"))
        result.append((f"\\\\\\{escape}", f"\\{unescaped}"))

    chars = "A1a\\\nøæå"
    for char in chars:
        code_point = ord(char)
        add_pair(f"u{code_point:04x}", char)
        add_pair(f"u{code_point:04X}", char)
        add_pair(f"U{code_point:08x}", char)
        add_pair(f"U{code_point:08X}", char)

    string_escapes = "tbnrf'"
    for char in string_escapes:
        add_pair(f"{char}", _string_escape_map[char])

    # special handling because «"» should not appear in string, and add_pair
    # will add it.
    result.append(('\\"', '"'))
    result.append(('\\\\\\"', '\\"'))

    # special handling because «\» should not appear in string, and add_pair
    # will add it.
    result.append(("\\\\", "\\"))
    result.append(("\\\\\\\\", "\\\\"))

    # reserved_escapes = "~.-!$&'()*+,;=/?#@%_"
    # for char in reserved_escapes:
    #     add_pair(f"{char}", char)

    return result


def test_check_data() -> None:
    test_data = make_test_data()
    for escaped, unescaped in test_data:
        logging.info("%r -> %r", escaped, unescaped)
    logging.info("make_test_data() = %s", make_test_data())


@pytest.mark.parametrize("escaped, unescaped", make_test_data())
def test_unquote_old(escaped: str, unescaped: str) -> None:
    logging.info("%r -> %r", escaped, unescaped)
    assert unescaped == unquote(escaped, False)


@pytest.mark.parametrize("escaped, unescaped", make_test_data())
def test_unquote_validate(escaped: str, unescaped: str) -> None:
    logging.info("%r -> %r", escaped, unescaped)
    assert unescaped == unquote(escaped, True)


@pytest.mark.parametrize("escaped, unescaped", make_test_data())
def test_unquote_new(escaped: str, unescaped: str) -> None:
    logging.info("%r -> %r", escaped, unescaped)
    assert unescaped == unquote(escaped, new=True)


# def test_turtle_unescaper() -> None:
#     logging.debug("EscapeGroup.__members__ = %s", EscapeGroup.__members__)
#     logging.debug("turtle_unescaper._pattern = %r", turtle_escape_pattern)
#     unescaped = unquote(r"\n - \u00AA - \u00bb - \U000000BB - \U000000aa - \#", new=True)
#     logging.debug("unescaped = %r", unescaped)

#     # TurtleUnescaper.unescape(r"\n - \u00AA - \U000000BB - \#")


# lorem_ipsum = """
# Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam nec malesuada dui. Nunc eu risus semper, porta turpis in, lacinia orci. Phasellus et fringilla elit. Aliquam at purus velit. Etiam turpis eros, bibendum eget lectus sit amet, porttitor pharetra risus. Integer non cursus nunc. Proin tristique placerat nibh, id ornare est lobortis quis. Maecenas eget magna vel nisl viverra hendrerit. Aliquam lacus tellus, posuere eget rhoncus non, mattis in diam. Proin volutpat quam nec finibus tempor. Quisque nisl leo, tempor et sodales ac, sollicitudin sed lacus. Sed nec quam eu elit malesuada suscipit.

# Cras mollis enim et molestie rhoncus. Nam eget maximus mi, in mollis tortor. Maecenas et nisi ac dolor euismod auctor. Duis ac ex dictum, lobortis ex quis, egestas nisl. Phasellus imperdiet, lectus sagittis dapibus scelerisque, dolor velit mollis neque, eu malesuada diam neque at tellus. Sed tellus nisl, rhoncus in quam eu, pulvinar fermentum enim. In ut orci ut arcu gravida varius in dapibus erat. Vestibulum efficitur velit in nisi posuere, laoreet molestie ante tempor. Cras ac pulvinar mauris. Vestibulum nec odio vehicula, mattis est vitae, eleifend sem. Ut luctus iaculis fermentum. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae;

# In consequat tempor justo quis sollicitudin. Phasellus aliquam erat a justo mollis fringilla sit amet ut purus. Nulla at dui vel ligula porttitor ullamcorper porta eu nibh. Sed imperdiet sem nibh, et maximus nisi tempus dignissim. Integer euismod nisl in lacinia pulvinar. Nulla hendrerit pretium lacus sed tincidunt. Donec vitae neque ac turpis lobortis eleifend. Aliquam semper arcu risus, quis venenatis odio interdum eu. Mauris felis mauris, vehicula sit amet tristique vitae, vehicula eu libero. Duis augue felis, vulputate ac velit sed, mattis condimentum metus. Duis ullamcorper magna nisl, id posuere est ultricies luctus. Quisque a urna ut sapien sodales pellentesque. Phasellus et viverra risus. Aliquam accumsan nisl ligula, vitae dapibus nibh rhoncus a. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Donec aliquam magna erat, sed euismod nibh dignissim a.

# Mauris feugiat justo id tempor ullamcorper. Donec dictum, lectus eu vulputate euismod, arcu sem pharetra sem, ac vulputate elit quam imperdiet turpis. In finibus, tortor sed finibus consequat, ante arcu hendrerit nunc, quis interdum nunc nisi et purus. Phasellus vel odio quis augue varius feugiat. Nulla feugiat nisi id magna condimentum, sed varius elit aliquam. Morbi dapibus, ante eu mollis consequat, arcu ex iaculis dolor, ac vulputate diam nunc vitae est. Suspendisse sit amet elementum dolor. Aenean tempor purus in tincidunt ultricies. Ut ac dui malesuada, tempus libero a, facilisis ex. Curabitur accumsan consectetur lorem non sagittis.

# Maecenas vehicula nisl in metus maximus, ut ornare orci consectetur. Sed vel felis ipsum. Sed condimentum, felis quis vulputate malesuada, nisi dui hendrerit sapien, interdum tincidunt lectus mauris at diam. Donec quis orci vel mi viverra rutrum non vitae nisi. Aliquam erat volutpat. Morbi quam lorem, volutpat ut augue id, mattis porttitor felis. Quisque tristique at lectus eu auctor. Aliquam pharetra viverra quam, quis lobortis lorem eleifend sed. Vivamus volutpat ipsum nulla, vel vestibulum lectus luctus nec. Vivamus interdum purus ac felis lacinia, non laoreet sapien commodo. Morbi turpis erat, malesuada vel neque eget, eleifend semper ex. Integer accumsan auctor nisl, nec sagittis orci porttitor dignissim. Interdum et malesuada fames ac ante ipsum primis in faucibus. Proin sit amet eros auctor, ultrices elit eu, suscipit sapien.
# """.replace(
#     "\n", r" "
# )


# def add_escapes(
#     input: str, escape_groups: List[EscapeGroup], chunk_size: int = 10
# ) -> str:
#     result = StringIO()
#     input_len = len(input)
#     chunk_count = math.ceil(input_len / chunk_size)
#     escape_group_count = len(escape_groups)
#     for chunk_index in range(chunk_count):
#         chunk = input[(chunk_index + 0) * chunk_size : (chunk_index + 1) * chunk_size]
#         # logging.info("chunk == %s", chunk)
#         result.write(chunk)
#         if escape_group_count == 0:
#             continue
#         escape_group = escape_groups[chunk_index % escape_group_count]
#         if escape_group == EscapeGroup.RESERVED:
#             result.write(f"\\{random.choice(reserved_escape_chars)}")
#         elif escape_group == EscapeGroup.STRING:
#             result.write(f"\\{random.choice('tbnrf')}")
#         elif escape_group == EscapeGroup.NARROW:
#             chars = "".join(random.choice("123456789abcdefABCDEF") for i in range(4))
#             result.write(f"\\u{chars}")
#         elif escape_group == EscapeGroup.WIDE:
#             chars = "".join(random.choice("123456789abcdefABCDEF") for i in range(4))
#             result.write(f"\\U0000{chars}")
#     return result.getvalue()


# test_strings_map: Dict[str, List[str]] = {
#     "no_escapes": [lorem_ipsum],
#     "few_escapes": [add_escapes(lorem_ipsum, list(EscapeGroup), 100)],
#     "many_escapes": [add_escapes(lorem_ipsum, list(EscapeGroup), 10)],
#     "many_escapes_string": [add_escapes(lorem_ipsum, [EscapeGroup.STRING], 10)],
#     "many_escapes_reserved": [add_escapes(lorem_ipsum, [EscapeGroup.RESERVED], 10)],
#     "many_escapes_narrow": [add_escapes(lorem_ipsum, [EscapeGroup.NARROW], 10)],
#     "many_escapes_wide": [add_escapes(lorem_ipsum, [EscapeGroup.WIDE], 10)],
# }


# def test_add_escapes() -> None:
#     assert add_escapes(lorem_ipsum, []) == lorem_ipsum
#     logging.info("%s", add_escapes(lorem_ipsum, list(EscapeGroup)))


# unescapers: Dict[str, Callable[[str], str]] = {
#     "decodeUnicodeEscape": lambda input: decodeUnicodeEscape(input),
#     "unquote_validate": lambda input: unquote(input, validate=True),
#     "turtle_unescape": lambda input: turtle_unescape(input),
# }


# def check_performance(
#     unescaper_key: str, test_strings_key: str, benchmark: BenchmarkFixture
# ) -> None:
#     unescaper = unescapers[unescaper_key]
#     test_strings = test_strings_map[test_strings_key]

#     def unquote_all() -> None:
#         for test_string in test_strings:
#             unescaper(test_string)

#     benchmark(unquote_all)


# # @pytest.mark.parametrize(
# #     "unescaper_key, test_strings_key",
# #     itertools.product(unescapers.keys(), test_strings_map.keys()),
# # )
# # def test_performance(
# #     unescaper_key: str,
# #     test_strings_key: str,
# #     benchmark: BenchmarkFixture,
# # ) -> None:
# #     check_performance(unescaper_key, test_strings_key, benchmark)


# @pytest.mark.parametrize("unescaper_key", unescapers.keys())
# def test_performance_no_escapes(unescaper_key: str, benchmark: BenchmarkFixture) -> None:
#     check_performance(unescaper_key, "no_escapes", benchmark)


# @pytest.mark.parametrize("unescaper_key", unescapers.keys())
# def test_performance_few_escaspes(unescaper_key: str, benchmark: BenchmarkFixture) -> None:
#     check_performance(unescaper_key, "few_escaspes", benchmark)


# @pytest.mark.parametrize("unescaper_key", unescapers.keys())
# def test_performance_many_escaspes(unescaper_key: str, benchmark: BenchmarkFixture) -> None:
#     check_performance(unescaper_key, "many_escaspes", benchmark)
