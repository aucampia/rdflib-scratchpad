import enum
import re
from typing import Match

string_escape_map = {
    "t": "\t",
    "b": "\b",
    "n": "\n",
    "r": "\r",
    "f": "\f",
    '"': '"',
    "'": "'",
    "\\": "\\",
}
string_escape_trans = str.maketrans(string_escape_map)


def _group_handler(match: Match[str]) -> str:
    rmatch, smatch, umatch = match.groups()
    if rmatch is not None:
        return rmatch
    elif smatch is not None:
        return smatch.translate(string_escape_trans)
    else:
        return chr(int(umatch[1:], 16))


turtle_escape_pattern = re.compile(
    r"""\\(?:([~.\-!$&'()*+,;=\/?#@%_])|([tbnrf"'\\])|(u[0-9A-Fa-f]{4}|U[0-9A-Fa-f]{8}))""",
    # re.ASCII,
)


def turtle_unescape(escaped: str) -> str:
    return turtle_escape_pattern.sub(_group_handler, escaped)


