import re
from typing import Match

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


def _turtle_escape_subber(match: Match[str]) -> str:
    smatch, umatch = match.groups()
    if smatch is not None:
        return smatch.translate(_string_escape_translator)
    else:
        return chr(int(umatch[1:], 16))


_turtle_escape_pattern = re.compile(
    r"""\\(?:([tbnrf"'\\])|(u[0-9A-Fa-f]{4}|U[0-9A-Fa-f]{8}))""",
    # re.ASCII,
)


def decodeUnicodeEscapeNew(escaped: str) -> str:
    if "\\" not in escaped:
        # Most of times, there are no backslashes in strings.
        # In the general case, it could use maketrans and translate.
        return escaped
    return _turtle_escape_pattern.sub(_turtle_escape_subber, escaped)


def _unicodeExpand(s: str) -> str:
    return r_unicodeEscape.sub(lambda m: chr(int(m.group(0)[2:], 16)), s)


def decodeUnicodeEscape(s: str) -> str:
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


def unquote(s: str, validate: bool = False, new: bool = False) -> str:
    """Unquote an N-Triples string."""
    if not validate:
        if new:
            return decodeUnicodeEscapeNew(s)
        else:
            if isinstance(s, str):  # nquads
                s = decodeUnicodeEscape(s)
            else:
                s = s.decode("unicode-escape")  # type: ignore[unreachable]

        return s
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
