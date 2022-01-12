import logging
import math
import random
from io import StringIO
from typing import Callable, List, Tuple

import pytest
import enum
from pytest_benchmark.fixture import BenchmarkFixture  # type: ignore[import]

from aucampia.rdflib.scratchpad.unescape import (
    turtle_unescape,
    string_escape_map,
    turtle_escape_pattern,
)

from aucampia.rdflib.scratchpad.unquote_fixed import decodeUnicodeEscape, unquote


class EscapeGroup(enum.Enum):
    RESERVED = 0
    STRING = 1
    UNICODE = 2
    NARROW = 3
    WIDE = 4


reserved_escape_chars = r"~.-!$&'()*+,;=/?#@%_"
string_escape_chars = r"""\tbnrf"'"""


# @pytest.mark.parametrize(
#     "quoted, unquoted",
#     [
#         (r"\n", "\n"),
#         (r"\r", "\r"),
#         (r"\\r", r"\r"),
#         (r"\\\r", "\\\r"),
#         (r"\u000D", "\r"),
#         (r"\\u000D", r"\u000D"),
#         (r"\U0000000D", "\r"),
#         (
#             r"\\U0000000D",
#             r"\U0000000D",
#         ),
#     ],
# )
# def test_unquote(quoted: str, unquoted: str) -> None:
#     assert unquoted == unquote(quoted)


# @pytest.mark.parametrize(
#     "quoted, unquoted",
#     [
#         (r"\n", "\n"),
#         (r"\r", "\r"),
#         (r"\\r", r"\r"),
#         (r"\\\r", "\\\r"),
#         ("\\u00e6", "æ"),
#         (r"\u00e6", "æ"),
#         (r"\u000D", "\r"),
#         (r"\\u000D", r"\u000D"),
#         (r"\U0000000D", "\r"),
#         (r"\\U0000000D", r"\U0000000D"),
#     ],
# )
# def test_unquote_validate(quoted: str, unquoted: str) -> None:
#     logging.info("%r -> %r", quoted, unquoted)
#     assert unquoted == unquote(quoted, True)


# def test_string_escape_decoder() -> None:
#     logging.info(
#         "string_escape_decoder.lookup_table = %s", string_escape_decoder.lookup_table
#     )


# @pytest.mark.parametrize("key, value", string_escape_map.items())
# def test_string_escape_decode(key: str, value: str) -> None:
#     assert repr(string_escape_decoder.lookup(key)) == repr(value)


# def compile_string_escape_map(map: Dict[str, str]) -> Tuple[int, int, Tuple[str, ...]]:
#     ords = [ord(key) for key in map.keys()]
#     min_key: int = min(ords)
#     max_key: int = max(ords)
#     # result = tuple([None] * (max_key - min_key))
#     result: List[str] = []
#     for key, value in map.items():
#         result[ord(key) - min_key] = value
#     return min_key, max_key, tuple(result)


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
        # result.append((f"\\u{code_point:04x}", char))
        # result.append((f"\\u{code_point:04x}", char))
        # result.append((f"\\u{code_point:04X}", char))
        # result.append((f"\\U{code_point:08x}", char))
        # result.append((f"\\U{code_point:08X}", char))

    string_escapes = "tbnrf'"
    for char in string_escapes:
        add_pair(f"{char}", string_escape_map[char])

    result.append(('\\"', '"'))
    result.append(('\\\\\\"', '\\"'))

    result.append(("\\\\", "\\"))
    result.append(("\\\\\\\\", "\\\\"))

    reserved_escapes = "~.-!$&'()*+,;=/?#@%_"
    for char in reserved_escapes:
        add_pair(f"{char}", char)

    return result


def test_check_data() -> None:
    test_data = make_test_data()
    for escaped, unescaped in test_data:
        logging.info("%r -> %r", escaped, unescaped)
    logging.info("make_test_data() = %s", make_test_data())


@pytest.mark.parametrize("escaped, unescaped", make_test_data())
def test_unquote(escaped: str, unescaped: str) -> None:
    logging.info("%r -> %r", escaped, unescaped)
    assert unescaped == unquote(escaped, False)


@pytest.mark.parametrize("escaped, unescaped", make_test_data())
def test_unquote_validate(escaped: str, unescaped: str) -> None:
    logging.info("%r -> %r", escaped, unescaped)
    assert unescaped == unquote(escaped, True)


@pytest.mark.parametrize("escaped, unescaped", make_test_data())
def test_unescape(escaped: str, unescaped: str) -> None:
    logging.info("%r -> %r", escaped, unescaped)
    assert unescaped == turtle_unescape(escaped)


def test_turtle_unescaper() -> None:
    logging.debug("EscapeGroup.__members__ = %s", EscapeGroup.__members__)
    logging.debug("turtle_unescaper._pattern = %r", turtle_escape_pattern)
    unescaped = turtle_unescape(r"\n - \u00AA - \u00bb - \U000000BB - \U000000aa - \#")
    logging.debug("unescaped = %r", unescaped)

    # TurtleUnescaper.unescape(r"\n - \u00AA - \U000000BB - \#")


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
        if escape_group == EscapeGroup.RESERVED:
            result.write(f"\\{random.choice(reserved_escape_chars)}")
        elif escape_group == EscapeGroup.STRING:
            result.write(f"\\{random.choice('tbnrf')}")
        # elif escape_group == EscapeGroup.UNICODE:
        #     if random.choice([True, False]):
        #         chars = "".join(random.choice("123456789abcdefABCDEF") for i in range(4))
        #         result.write(f"\\w{chars}")
        #     else:
        #         chars = "".join(random.choice("123456789abcdefABCDEF") for i in range(8))
        #         result.write(f"\\W{chars}")
        elif escape_group == EscapeGroup.NARROW:
            chars = "".join(random.choice("123456789abcdefABCDEF") for i in range(4))
            result.write(f"\\u{chars}")
        elif escape_group == EscapeGroup.WIDE:
            chars = "".join(random.choice("123456789abcdefABCDEF") for i in range(4))
            result.write(f"\\U0000{chars}")
    return result.getvalue()


def test_add_escapes() -> None:
    assert add_escapes(lorem_ipsum, []) == lorem_ipsum
    logging.info("%s", add_escapes(lorem_ipsum, list(EscapeGroup)))


@pytest.mark.parametrize(
    "unescaper, escaped_strings",
    [
        pytest.param(
            lambda input: decodeUnicodeEscape(input),
            [lorem_ipsum],
            id="decodeUnicodeEscape/plain",
        ),
        pytest.param(
            lambda input: unquote(input, validate=True),
            [lorem_ipsum],
            id="unquote/validate=True/plain",
        ),
        pytest.param(
            lambda input: turtle_unescape(input),
            [lorem_ipsum],
            id="unescape/plain",
        ),
        pytest.param(
            lambda input: decodeUnicodeEscape(input),
            [add_escapes(lorem_ipsum, list(EscapeGroup))],
            id="decodeUnicodeEscape/escaped",
        ),
        pytest.param(
            lambda input: unquote(input, validate=True),
            [add_escapes(lorem_ipsum, list(EscapeGroup))],
            id="unquote/validate=True/escaped",
        ),
        pytest.param(
            lambda input: turtle_unescape(input),
            [add_escapes(lorem_ipsum, list(EscapeGroup))],
            id="unescape/escaped",
        ),
        pytest.param(
            lambda input: decodeUnicodeEscape(input),
            [add_escapes(lorem_ipsum, [EscapeGroup.STRING])],
            id="decodeUnicodeEscape/string",
        ),
        pytest.param(
            lambda input: unquote(input, validate=True),
            [add_escapes(lorem_ipsum, [EscapeGroup.STRING])],
            id="unquote/validate=True/string",
        ),
        pytest.param(
            lambda input: turtle_unescape(input),
            [add_escapes(lorem_ipsum, [EscapeGroup.STRING])],
            id="unescape/string",
        ),
    ],
)
def test_performance(
    unescaper: Callable[[str], str],
    escaped_strings: List[str],
    benchmark: BenchmarkFixture,
) -> None:
    def unquote_all() -> None:
        for escaped_string in escaped_strings:
            unescaper(escaped_string)

    benchmark(unquote_all)
    # benchmark.pedantic(unquote_all, iterations=20, rounds=4000)


# def test_performance_unquote(benchmark: BenchmarkFixture) -> None:
#     def unquote_all() -> None:
#         for raw_string in raw_strings:
#             unquote(raw_string, validate=False)

#     benchmark(unquote_all)


# def test_performance_unquote_validate(benchmark: BenchmarkFixture) -> None:
#     def unquote_all() -> None:
#         for raw_string in raw_strings:
#             unquote(raw_string, validate=True)

#     benchmark(unquote_all)
#     # logging.info("benchmark = %s", benchmark)


# def test_performance_turtle_unescaper(benchmark: BenchmarkFixture) -> None:
#     def unquote_all() -> None:
#         for raw_string in raw_strings:
#             turtle_unescaper.unescape(raw_string)

#     benchmark(unquote_all)
