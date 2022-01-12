import logging
import os

from pytest_subtests import SubTests  # type: ignore[import]


def test_something(subtests: SubTests) -> None:
    logging.info("entry: ...")
    assert "" != os.name

    with subtests.test(msg="something"):
        assert "" != os.name
