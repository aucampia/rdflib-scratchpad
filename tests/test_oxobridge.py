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


"""
20231027T010801W43 iwana@teekai.zoic.eu.org:~/sw/d/github.com/aucampia/rdflib-scratchpad
$ task test -- --log-cli-level DEBUG
task: [test] poetry run python -m pytest --log-cli-level DEBUG
============================================================================ test session starts ============================================================================
platform linux -- Python 3.11.6, pytest-7.4.3, pluggy-1.3.0
rootdir: /home/iwana/sw/d/github.com/aucampia/rdflib-scratchpad
configfile: pyproject.toml
testpaths: tests
plugins: cov-4.1.0
collected 1 item

tests/test_oxobridge.py::test_bridge
------------------------------------------------------------------------------- live log call -------------------------------------------------------------------------------
2023-10-27T01:08:04 683672 140592927643456 010:DEBUG    root         test_oxobridge:32:test_bridge buffer = <http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#object> <http://www.w3.org/2000/01/rdf-schema#comment> "The object of the subject RDF statement." }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#object> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#object> <http://www.w3.org/2000/01/rdf-schema#range> <http://www.w3.org/2000/01/rdf-schema#Resource> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#object> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/1999/02/22-rdf-syntax-ns#> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#object> <http://www.w3.org/2000/01/rdf-schema#domain> <http://www.w3.org/1999/02/22-rdf-syntax-ns#Statement> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#object> <http://www.w3.org/2000/01/rdf-schema#label> "object" }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#> <http://purl.org/dc/elements/1.1/title> "The RDF Concepts Vocabulary (RDF)" }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#> <http://purl.org/dc/elements/1.1/description> "This is the RDF Schema for the RDF vocabulary terms in the RDF Namespace, defined in RDF 1.1 Concepts." }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Ontology> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#> <http://purl.org/dc/elements/1.1/date> "2019-12-16" }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#XMLLiteral> <http://www.w3.org/2000/01/rdf-schema#comment> "The datatype of XML literal values." }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#XMLLiteral> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Datatype> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#XMLLiteral> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://www.w3.org/2000/01/rdf-schema#Literal> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#XMLLiteral> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/1999/02/22-rdf-syntax-ns#> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#XMLLiteral> <http://www.w3.org/2000/01/rdf-schema#label> "XMLLiteral" }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#value> <http://www.w3.org/2000/01/rdf-schema#comment> "Idiomatic property used for structured values." }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#value> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#value> <http://www.w3.org/2000/01/rdf-schema#range> <http://www.w3.org/2000/01/rdf-schema#Resource> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#value> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/1999/02/22-rdf-syntax-ns#> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#value> <http://www.w3.org/2000/01/rdf-schema#domain> <http://www.w3.org/2000/01/rdf-schema#Resource> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#value> <http://www.w3.org/2000/01/rdf-schema#label> "value" }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#Statement> <http://www.w3.org/2000/01/rdf-schema#comment> "The class of RDF statements." }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#Statement> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Class> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#Statement> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://www.w3.org/2000/01/rdf-schema#Resource> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#Statement> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/1999/02/22-rdf-syntax-ns#> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#Statement> <http://www.w3.org/2000/01/rdf-schema#label> "Statement" }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral> <http://www.w3.org/2000/01/rdf-schema#comment> "The class of plain (i.e. untyped) literal values, as used in RIF and OWL 2" }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Datatype> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral> <http://www.w3.org/2000/01/rdf-schema#seeAlso> <http://www.w3.org/TR/rdf-plain-literal/> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://www.w3.org/2000/01/rdf-schema#Literal> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/1999/02/22-rdf-syntax-ns#> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#PlainLiteral> <http://www.w3.org/2000/01/rdf-schema#label> "PlainLiteral" }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#comment> "The subject is an instance of a class." }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#range> <http://www.w3.org/2000/01/rdf-schema#Class> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/1999/02/22-rdf-syntax-ns#> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#domain> <http://www.w3.org/2000/01/rdf-schema#Resource> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#label> "type" }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#rest> <http://www.w3.org/2000/01/rdf-schema#comment> "The rest of the subject RDF list after the first item." }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#rest> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#rest> <http://www.w3.org/2000/01/rdf-schema#range> <http://www.w3.org/1999/02/22-rdf-syntax-ns#List> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#rest> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/1999/02/22-rdf-syntax-ns#> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#rest> <http://www.w3.org/2000/01/rdf-schema#domain> <http://www.w3.org/1999/02/22-rdf-syntax-ns#List> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#rest> <http://www.w3.org/2000/01/rdf-schema#label> "rest" }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#language> <http://www.w3.org/2000/01/rdf-schema#comment> "The language component of a CompoundLiteral." }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#language> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#language> <http://www.w3.org/2000/01/rdf-schema#seeAlso> <https://www.w3.org/TR/json-ld11/#the-rdf-compoundliteral-class-and-the-rdf-language-and-rdf-direction-properties> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#language> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/1999/02/22-rdf-syntax-ns#> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#language> <http://www.w3.org/2000/01/rdf-schema#domain> <http://www.w3.org/1999/02/22-rdf-syntax-ns#CompoundLiteral> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#language> <http://www.w3.org/2000/01/rdf-schema#label> "language" }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#first> <http://www.w3.org/2000/01/rdf-schema#comment> "The first item in the subject RDF list." }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#first> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#first> <http://www.w3.org/2000/01/rdf-schema#range> <http://www.w3.org/2000/01/rdf-schema#Resource> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#first> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/1999/02/22-rdf-syntax-ns#> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#first> <http://www.w3.org/2000/01/rdf-schema#domain> <http://www.w3.org/1999/02/22-rdf-syntax-ns#List> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#first> <http://www.w3.org/2000/01/rdf-schema#label> "first" }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate> <http://www.w3.org/2000/01/rdf-schema#comment> "The predicate of the subject RDF statement." }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate> <http://www.w3.org/2000/01/rdf-schema#range> <http://www.w3.org/2000/01/rdf-schema#Resource> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/1999/02/22-rdf-syntax-ns#> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate> <http://www.w3.org/2000/01/rdf-schema#domain> <http://www.w3.org/1999/02/22-rdf-syntax-ns#Statement> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#predicate> <http://www.w3.org/2000/01/rdf-schema#label> "predicate" }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#Alt> <http://www.w3.org/2000/01/rdf-schema#comment> "The class of containers of alternatives." }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#Alt> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Class> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#Alt> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://www.w3.org/2000/01/rdf-schema#Container> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#Alt> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/1999/02/22-rdf-syntax-ns#> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#Alt> <http://www.w3.org/2000/01/rdf-schema#label> "Alt" }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> <http://www.w3.org/2000/01/rdf-schema#comment> "The class of RDF properties." }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Class> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://www.w3.org/2000/01/rdf-schema#Resource> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/1999/02/22-rdf-syntax-ns#> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> <http://www.w3.org/2000/01/rdf-schema#label> "Property" }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#nil> <http://www.w3.org/2000/01/rdf-schema#comment> "The empty list, with no items in it. If the rest of a list is nil then the list has no more items in it." }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#nil> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/1999/02/22-rdf-syntax-ns#List> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#nil> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/1999/02/22-rdf-syntax-ns#> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#nil> <http://www.w3.org/2000/01/rdf-schema#label> "nil" }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#direction> <http://www.w3.org/2000/01/rdf-schema#comment> "The base direction component of a CompoundLiteral." }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#direction> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#direction> <http://www.w3.org/2000/01/rdf-schema#seeAlso> <https://www.w3.org/TR/json-ld11/#the-rdf-compoundliteral-class-and-the-rdf-language-and-rdf-direction-properties> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#direction> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/1999/02/22-rdf-syntax-ns#> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#direction> <http://www.w3.org/2000/01/rdf-schema#domain> <http://www.w3.org/1999/02/22-rdf-syntax-ns#CompoundLiteral> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#direction> <http://www.w3.org/2000/01/rdf-schema#label> "direction" }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#langString> <http://www.w3.org/2000/01/rdf-schema#comment> "The datatype of language-tagged string values" }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#langString> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Datatype> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#langString> <http://www.w3.org/2000/01/rdf-schema#seeAlso> <http://www.w3.org/TR/rdf11-concepts/#section-Graph-Literal> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#langString> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://www.w3.org/2000/01/rdf-schema#Literal> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#langString> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/1999/02/22-rdf-syntax-ns#> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#langString> <http://www.w3.org/2000/01/rdf-schema#label> "langString" }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#Seq> <http://www.w3.org/2000/01/rdf-schema#comment> "The class of ordered containers." }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#Seq> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Class> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#Seq> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://www.w3.org/2000/01/rdf-schema#Container> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#Seq> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/1999/02/22-rdf-syntax-ns#> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#Seq> <http://www.w3.org/2000/01/rdf-schema#label> "Seq" }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#Bag> <http://www.w3.org/2000/01/rdf-schema#comment> "The class of unordered containers." }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#Bag> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Class> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#Bag> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://www.w3.org/2000/01/rdf-schema#Container> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#Bag> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/1999/02/22-rdf-syntax-ns#> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#Bag> <http://www.w3.org/2000/01/rdf-schema#label> "Bag" }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#subject> <http://www.w3.org/2000/01/rdf-schema#comment> "The subject of the subject RDF statement." }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#subject> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#subject> <http://www.w3.org/2000/01/rdf-schema#range> <http://www.w3.org/2000/01/rdf-schema#Resource> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#subject> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/1999/02/22-rdf-syntax-ns#> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#subject> <http://www.w3.org/2000/01/rdf-schema#domain> <http://www.w3.org/1999/02/22-rdf-syntax-ns#Statement> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#subject> <http://www.w3.org/2000/01/rdf-schema#label> "subject" }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#JSON> <http://www.w3.org/2000/01/rdf-schema#comment> "The datatype of RDF literals storing JSON content." }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#JSON> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Datatype> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#JSON> <http://www.w3.org/2000/01/rdf-schema#seeAlso> <https://www.w3.org/TR/json-ld11/#the-rdf-json-datatype> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#JSON> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://www.w3.org/2000/01/rdf-schema#Literal> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#JSON> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/1999/02/22-rdf-syntax-ns#> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#JSON> <http://www.w3.org/2000/01/rdf-schema#label> "JSON" }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#CompoundLiteral> <http://www.w3.org/2000/01/rdf-schema#comment> "A class representing a compound literal." }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#CompoundLiteral> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Class> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#CompoundLiteral> <http://www.w3.org/2000/01/rdf-schema#seeAlso> <https://www.w3.org/TR/json-ld11/#the-rdf-compoundliteral-class-and-the-rdf-language-and-rdf-direction-properties> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#CompoundLiteral> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://www.w3.org/2000/01/rdf-schema#Resource> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#CompoundLiteral> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/1999/02/22-rdf-syntax-ns#> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#CompoundLiteral> <http://www.w3.org/2000/01/rdf-schema#label> "CompoundLiteral" }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#List> <http://www.w3.org/2000/01/rdf-schema#comment> "The class of RDF Lists." }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#List> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Class> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#List> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://www.w3.org/2000/01/rdf-schema#Resource> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#List> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/1999/02/22-rdf-syntax-ns#> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#List> <http://www.w3.org/2000/01/rdf-schema#label> "List" }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#HTML> <http://www.w3.org/2000/01/rdf-schema#comment> "The datatype of RDF literals storing fragments of HTML content" }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#HTML> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Datatype> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#HTML> <http://www.w3.org/2000/01/rdf-schema#seeAlso> <http://www.w3.org/TR/rdf11-concepts/#section-html> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#HTML> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://www.w3.org/2000/01/rdf-schema#Literal> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#HTML> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/1999/02/22-rdf-syntax-ns#> }
<http://example.com/rdf> { <http://www.w3.org/1999/02/22-rdf-syntax-ns#HTML> <http://www.w3.org/2000/01/rdf-schema#label> "HTML" }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#Datatype> <http://www.w3.org/2000/01/rdf-schema#comment> "The class of RDF datatypes." }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#Datatype> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Class> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#Datatype> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://www.w3.org/2000/01/rdf-schema#Class> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#Datatype> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/2000/01/rdf-schema#> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#Datatype> <http://www.w3.org/2000/01/rdf-schema#label> "Datatype" }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#subPropertyOf> <http://www.w3.org/2000/01/rdf-schema#comment> "The subject is a subproperty of a property." }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#subPropertyOf> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#subPropertyOf> <http://www.w3.org/2000/01/rdf-schema#range> <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#subPropertyOf> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/2000/01/rdf-schema#> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#subPropertyOf> <http://www.w3.org/2000/01/rdf-schema#domain> <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#subPropertyOf> <http://www.w3.org/2000/01/rdf-schema#label> "subPropertyOf" }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#comment> <http://www.w3.org/2000/01/rdf-schema#comment> "A description of the subject resource." }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#comment> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#comment> <http://www.w3.org/2000/01/rdf-schema#range> <http://www.w3.org/2000/01/rdf-schema#Literal> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#comment> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/2000/01/rdf-schema#> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#comment> <http://www.w3.org/2000/01/rdf-schema#domain> <http://www.w3.org/2000/01/rdf-schema#Resource> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#comment> <http://www.w3.org/2000/01/rdf-schema#label> "comment" }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#seeAlso> <http://www.w3.org/2000/01/rdf-schema#comment> "Further information about the subject resource." }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#seeAlso> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#seeAlso> <http://www.w3.org/2000/01/rdf-schema#range> <http://www.w3.org/2000/01/rdf-schema#Resource> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#seeAlso> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/2000/01/rdf-schema#> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#seeAlso> <http://www.w3.org/2000/01/rdf-schema#domain> <http://www.w3.org/2000/01/rdf-schema#Resource> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#seeAlso> <http://www.w3.org/2000/01/rdf-schema#label> "seeAlso" }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#member> <http://www.w3.org/2000/01/rdf-schema#comment> "A member of the subject resource." }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#member> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#member> <http://www.w3.org/2000/01/rdf-schema#range> <http://www.w3.org/2000/01/rdf-schema#Resource> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#member> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/2000/01/rdf-schema#> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#member> <http://www.w3.org/2000/01/rdf-schema#domain> <http://www.w3.org/2000/01/rdf-schema#Resource> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#member> <http://www.w3.org/2000/01/rdf-schema#label> "member" }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#> <http://purl.org/dc/elements/1.1/title> "The RDF Schema vocabulary (RDFS)" }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2002/07/owl#Ontology> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#> <http://www.w3.org/2000/01/rdf-schema#seeAlso> <http://www.w3.org/2000/01/rdf-schema-more> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#Container> <http://www.w3.org/2000/01/rdf-schema#comment> "The class of RDF containers." }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#Container> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Class> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#Container> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://www.w3.org/2000/01/rdf-schema#Resource> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#Container> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/2000/01/rdf-schema#> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#Container> <http://www.w3.org/2000/01/rdf-schema#label> "Container" }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#ContainerMembershipProperty> <http://www.w3.org/2000/01/rdf-schema#comment> "The class of container membership properties, rdf:_1, rdf:_2, ...,\n                    all of which are sub-properties of 'member'." }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#ContainerMembershipProperty> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Class> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#ContainerMembershipProperty> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#ContainerMembershipProperty> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/2000/01/rdf-schema#> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#ContainerMembershipProperty> <http://www.w3.org/2000/01/rdf-schema#label> "ContainerMembershipProperty" }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#range> <http://www.w3.org/2000/01/rdf-schema#comment> "A range of the subject property." }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#range> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#range> <http://www.w3.org/2000/01/rdf-schema#range> <http://www.w3.org/2000/01/rdf-schema#Class> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#range> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/2000/01/rdf-schema#> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#range> <http://www.w3.org/2000/01/rdf-schema#domain> <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#range> <http://www.w3.org/2000/01/rdf-schema#label> "range" }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#Literal> <http://www.w3.org/2000/01/rdf-schema#comment> "The class of literal values, eg. textual strings and integers." }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#Literal> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Class> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#Literal> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://www.w3.org/2000/01/rdf-schema#Resource> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#Literal> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/2000/01/rdf-schema#> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#Literal> <http://www.w3.org/2000/01/rdf-schema#label> "Literal" }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://www.w3.org/2000/01/rdf-schema#comment> "The subject is a subclass of a class." }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://www.w3.org/2000/01/rdf-schema#range> <http://www.w3.org/2000/01/rdf-schema#Class> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/2000/01/rdf-schema#> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://www.w3.org/2000/01/rdf-schema#domain> <http://www.w3.org/2000/01/rdf-schema#Class> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://www.w3.org/2000/01/rdf-schema#label> "subClassOf" }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#Resource> <http://www.w3.org/2000/01/rdf-schema#comment> "The class resource, everything." }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#Resource> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Class> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#Resource> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/2000/01/rdf-schema#> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#Resource> <http://www.w3.org/2000/01/rdf-schema#label> "Resource" }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#Class> <http://www.w3.org/2000/01/rdf-schema#comment> "The class of classes." }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#Class> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/2000/01/rdf-schema#Class> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#Class> <http://www.w3.org/2000/01/rdf-schema#subClassOf> <http://www.w3.org/2000/01/rdf-schema#Resource> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#Class> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/2000/01/rdf-schema#> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#Class> <http://www.w3.org/2000/01/rdf-schema#label> "Class" }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/2000/01/rdf-schema#subPropertyOf> <http://www.w3.org/2000/01/rdf-schema#seeAlso> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/2000/01/rdf-schema#comment> "The defininition of the subject resource." }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/2000/01/rdf-schema#range> <http://www.w3.org/2000/01/rdf-schema#Resource> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/2000/01/rdf-schema#> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/2000/01/rdf-schema#domain> <http://www.w3.org/2000/01/rdf-schema#Resource> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/2000/01/rdf-schema#label> "isDefinedBy" }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#domain> <http://www.w3.org/2000/01/rdf-schema#comment> "A domain of the subject property." }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#domain> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#domain> <http://www.w3.org/2000/01/rdf-schema#range> <http://www.w3.org/2000/01/rdf-schema#Class> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#domain> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/2000/01/rdf-schema#> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#domain> <http://www.w3.org/2000/01/rdf-schema#domain> <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#domain> <http://www.w3.org/2000/01/rdf-schema#label> "domain" }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#label> <http://www.w3.org/2000/01/rdf-schema#comment> "A human-readable name for the subject." }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#label> <http://www.w3.org/1999/02/22-rdf-syntax-ns#type> <http://www.w3.org/1999/02/22-rdf-syntax-ns#Property> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#label> <http://www.w3.org/2000/01/rdf-schema#range> <http://www.w3.org/2000/01/rdf-schema#Literal> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#label> <http://www.w3.org/2000/01/rdf-schema#isDefinedBy> <http://www.w3.org/2000/01/rdf-schema#> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#label> <http://www.w3.org/2000/01/rdf-schema#domain> <http://www.w3.org/2000/01/rdf-schema#Resource> }
<http://example.com/rdfs> { <http://www.w3.org/2000/01/rdf-schema#label> <http://www.w3.org/2000/01/rdf-schema#label> "label" }

PASSED                                                                                                                                                                [100%]/home/iwana/.cache/pypoetry/virtualenvs/rdflib-scratchpad-YdyGCH0m-py3.11/lib64/python3.11/site-packages/coverage/control.py:883: CoverageWarning: No data was collected. (no-data-collected)
  self._warn("No data was collected.", slug="no-data-collected")
WARNING: Failed to generate report: No data to report.

/home/iwana/.cache/pypoetry/virtualenvs/rdflib-scratchpad-YdyGCH0m-py3.11/lib/python3.11/site-packages/pytest_cov/plugin.py:312: CovReportWarning: Failed to generate report: No data to report.

  warnings.warn(CovReportWarning(message))


---------- coverage: platform linux, python 3.11.6-final-0 -----------


============================================================================= 1 passed in 0.24s =============================================================================
"""
