from rdflib import XSD, Graph, Literal, Namespace, URIRef
import logging
from rfc3986 import IRIReference, urlparse, ParseResult, uri_reference, iri_reference

EGNS = Namespace("http://example.com/")


def test_blank_datatype() -> None:
    graph = Graph()

    t1 = (EGNS.subj, EGNS.pred, Literal("obj1", datatype=""))
    assert t1[2].datatype == ""
    t2 = (EGNS.subj, EGNS.pred, Literal("obj2", None))
    assert t2[2].datatype is None
    t3 = (EGNS.subj, EGNS.pred, Literal("obj3", datatype=XSD.string))
    assert t3[2].datatype == XSD.string
    graph.add(t1)
    graph.add(t2)
    graph.add(t3)

    data = graph.serialize()
    logging.info("data = %s", data)

    blank_uri = URIRef("")

    pr = urlparse("")
    pr.encode()
    ir = iri_reference("")

