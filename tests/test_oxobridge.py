import io
import logging
from pathlib import Path
import sys
from typing import Iterable
from oxrdflib import OxigraphStore
import rdflib
import pyoxigraph

EGDC = rdflib.Namespace("http://example.com/")


TEST_DATA_DIR = Path(__file__).parent / "data"


def test_bridge() -> None:
    dataset = rdflib.Dataset(store="Oxigraph")
    dataset.get_context(EGDC["rdfs"]).parse(TEST_DATA_DIR / "rdfs.ttl", format="ttl")
    store = dataset.store
    assert isinstance(store, OxigraphStore)

    def data_iterator() -> Iterable[pyoxigraph.Quad]:
        for item in pyoxigraph.parse(Path(TEST_DATA_DIR / "rdf.ttl"), "text/turtle"):
            # quad.graph_name = pyoxigraph.NamedNode(EGDC["rdf"])
            yield pyoxigraph.Quad(item.subject, item.predicate, item.object, pyoxigraph.NamedNode(EGDC["rdf"]))

    store._inner.extend(data_iterator())

    buffer = io.BytesIO()
    store._inner.dump(buffer, mime_type="application/trig")

    logging.debug("buffer = %s", buffer.getvalue().decode("utf8"))
