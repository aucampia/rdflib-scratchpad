import re
from typing import Callable, Dict, Match

r_unicodeEscape = re.compile(r"(\\u[0-9A-Fa-f]{4}|\\U[0-9A-Fa-f]{8})")


_string_escape_map = {
    "t": "\t",
    "b": "\b",
    "n": "\n",
    "r": "\r",
    "f": "\f",
    '"': '"',
    "'": "'",
    "\\": "\\",
}
_string_escape_translator = str.maketrans(_string_escape_map)


_turtle_escape_pattern = re.compile(
    r"""\\(?:([tbnrf"'\\])|(u[0-9A-Fa-f]{4}|U[0-9A-Fa-f]{8}))""",
    # re.ASCII,
)

# smatch_variant: Dict[int, Callable[[str], str]] = {
#     1: lambda smatch: smatch.translate(_string_escape_translator),
#     2: lambda smatch: _string_escape_map[smatch],
# }


def _turtle_escape_subber(match: Match[str], variant: int) -> str:
    smatch, umatch = match.groups()
    if smatch is not None:
        return _string_escape_map[smatch]
        # return smatch_variant[variant](smatch)
        # if variant == 1:
        #     return smatch.translate(_string_escape_translator)
        # if variant == 2:
        #     return _string_escape_map[smatch]
    else:
        return chr(int(umatch[1:], 16))


def decodeUnicodeEscapeNew(escaped: str, variant: int) -> str:
    if "\\" not in escaped:
        # Most of times, there are no backslashes in strings.
        # In the general case, it could use maketrans and translate.
        return escaped
    return _turtle_escape_pattern.sub(
        lambda match: _turtle_escape_subber(match, variant), escaped
    )


# def _turtle_escape_subber_dict(match: Match[str]) -> str:
#     smatch, umatch = match.groups()
#     if smatch is not None:
#         return _string_escape_map[smatch]
#     else:
#         return chr(int(umatch[1:], 16))


# def decodeUnicodeEscapeNewDict(escaped: str) -> str:
#     if "\\" not in escaped:
#         # Most of times, there are no backslashes in strings.
#         # In the general case, it could use maketrans and translate.
#         return escaped
#     return _turtle_escape_pattern.sub(_turtle_escape_subber_dict, escaped)


# def _turtle_escape_subber(match: Match[str]) -> str:
#     smatch, umatch = match.groups()
#     if smatch is not None:
#         return smatch.translate(_string_escape_translator)
#     else:
#         return chr(int(umatch[1:], 16))


# def decodeUnicodeEscapeNew(escaped: str) -> str:
#     if "\\" not in escaped:
#         # Most of times, there are no backslashes in strings.
#         # In the general case, it could use maketrans and translate.
#         return escaped
#     return _turtle_escape_pattern.sub(_turtle_escape_subber, escaped)


def _unicodeExpand(s: str) -> str:
    return r_unicodeEscape.sub(lambda m: chr(int(m.group(0)[2:], 16)), s)


def decodeUnicodeEscape(s: str, variant: int) -> str:
    """
    s is a unicode string
    replace ``\\n`` and ``\\u00AC`` unicode escapes
    """
    if "\\" not in s:
        # Most of times, there are no backslashes in strings.
        # In the general case, it could use maketrans and translate.
        return s

    s = s.replace("\\t", "\t")
    s = s.replace("\\n", "\n")
    s = s.replace("\\r", "\r")
    s = s.replace("\\b", "\b")
    s = s.replace("\\f", "\f")
    s = s.replace('\\"', '"')
    s = s.replace("\\'", "'")
    s = s.replace("\\\\", "\\")

    s = _unicodeExpand(s)  # hmm - string escape doesn't do unicode escaping

    return s


# quot = {"t": "\t", "n": "\n", "r": "\r", '"': '"', "\\": "\\"}
r_safe = re.compile(r"([\x20\x21\x23-\x5B\x5D-\x7E]+)")
# r_quot = re.compile(r'\\(t|n|r|"|\\)')
r_quot = re.compile(r"""\\([tbnrf"'\\])""")
r_uniquot = re.compile(r"\\u([0-9A-Fa-f]{4})|\\U([0-9A-Fa-f]{8})")


variants = {
    0: decodeUnicodeEscape,
    1: decodeUnicodeEscapeNew,
    # 2: decodeUnicodeEscapeNew,
}


def unquote(s: str, validate: bool, variant: int) -> str:
    """Unquote an N-Triples string."""
    if not validate:
        # if variant == 0:
        #     if isinstance(s, str):  # nquads
        #         s = decodeUnicodeEscape(s)
        #     else:
        #         s = s.decode("unicode-escape")  # type: ignore[unreachable]
        # elif variant == 1:
        #     return decodeUnicodeEscapeNew(s)
        # elif variant == 2:
        #     return decodeUnicodeEscapeNewDict(s)
        # else:

        return variants[variant](s, variant)
    else:
        result = []
        while s:
            m = r_safe.match(s)
            if m:
                s = s[m.end() :]
                result.append(m.group(1))
                continue

            m = r_quot.match(s)
            if m:
                s = s[2:]
                # result.append(quot[m.group(1)])
                result.append(m.group(1).translate(_string_escape_translator))
                continue

            m = r_uniquot.match(s)
            if m:
                s = s[m.end() :]
                u, U = m.groups()
                codepoint = int(u or U, 16)
                if codepoint > 0x10FFFF:
                    raise ValueError("Disallowed codepoint: %08X" % codepoint)
                result.append(chr(codepoint))

            elif s.startswith("\\"):
                raise ValueError("Illegal escape at: %s..." % s[:10])
            else:
                raise ValueError("Illegal literal character: %r" % s[0])
        return "".join(result)
