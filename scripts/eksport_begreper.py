# /// script
# requires-python = ">=3.10"
# dependencies = ["linkml==1.9.5", "linkml-runtime==1.9.5", "rdflib==7.4.0", "jsonschema==4.25.1", "PyYAML==6.0.3"]
# ///
"""Validate the example concept data and export its SKOS-AP-NO subset as Turtle."""

import argparse
import json
from pathlib import Path
import sys
from urllib.parse import quote

import jsonschema
from linkml.generators.jsonschemagen import JsonSchemaGenerator
from rdflib import BNode, Graph, Literal, Namespace, URIRef
from rdflib.namespace import DCAT, DCTERMS, RDF, RDFS, SKOS, XSD
import yaml


SCHEMA = Path(__file__).resolve().parents[1] / "models/eksempel/begrepsmodell.yaml"
SKOSNO = Namespace("https://data.norge.no/vocabulary/skosno#")
XKOS = Namespace("http://rdf-vocabulary.ddialliance.org/xkos#")
ORG = Namespace("http://www.w3.org/ns/org#")
VCARD = Namespace("http://www.w3.org/2006/vcard/ns#")


def validate_data(data):
    schema = json.loads(JsonSchemaGenerator(str(SCHEMA)).serialize())
    # LinkML 1.9.5 leaves Unicode names unescaped in JSON Schema URI references.
    # Encode the references while keeping the class names and $defs keys intact.
    def encode_references(node):
        if isinstance(node, dict):
            for key, value in node.items():
                if key == "$ref":
                    node[key] = quote(value, safe="/:#%?=&~$")
                else:
                    encode_references(value)
        elif isinstance(node, list):
            for value in node:
                encode_references(value)

    encode_references(schema)
    jsonschema.validate(data, schema)
    identifiers = [concept["id"] for concept in data["begreper"]]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("Begrepene må ha unike identifikatorer.")
    for concept in data["begreper"]:
        targets = list(concept.get("overbegreper", []))
        targets.extend(relation["tilBegrep"] for relation in concept.get("assosiativeRelasjoner", []))
        for target in targets:
            if target not in identifiers:
                raise ValueError(f"Ukjent begrepsreferanse i denne eksempelsamlingen: {target}")


def to_rdf(data):
    validate_data(data)
    graph = Graph()
    for prefix, namespace in (("skosno", SKOSNO), ("xkos", XKOS), ("org", ORG), ("vcard", VCARD)):
        graph.bind(prefix, namespace)

    def language_literals(subject, predicate, texts):
        for language, text in texts.items():
            graph.add((subject, predicate, Literal(text, lang=language)))

    def resource(record, rdf_type):
        subject = URIRef(record["id"])
        graph.add((subject, RDF.type, rdf_type))
        graph.add((subject, DCTERMS.identifier, Literal(record["id"], datatype=XSD.anyURI)))
        publisher = record["utgiver"]
        publisher_uri = URIRef(publisher["id"])
        graph.add((subject, DCTERMS.publisher, publisher_uri))
        graph.add((publisher_uri, RDF.type, ORG.Organization))
        graph.add((publisher_uri, RDFS.label, Literal(publisher["navn"], lang="nb")))
        contact = record["kontaktpunkt"]
        contact_uri = URIRef(contact["id"])
        graph.add((subject, DCAT.contactPoint, contact_uri))
        graph.add((contact_uri, RDF.type, VCARD.Group))
        graph.add((contact_uri, VCARD.fn, Literal(contact["navn"], lang="nb")))
        graph.add((contact_uri, VCARD.hasEmail, URIRef(contact["epost"])))
        return subject

    collection = resource(data, SKOS.Collection)
    language_literals(collection, DCTERMS.title, data["navn"])
    for concept in data["begreper"]:
        subject = resource(concept, SKOS.Concept)
        graph.add((collection, SKOS.member, subject))
        language_literals(subject, SKOS.prefLabel, concept["anbefaltTerm"])
        language_literals(subject, SKOS.definition, concept["definisjon"])
        for parent in concept.get("overbegreper", []):
            graph.add((subject, XKOS.specializes, URIRef(parent)))
            graph.add((URIRef(parent), XKOS.generalizes, subject))
        for relation in concept.get("assosiativeRelasjoner", []):
            relation_node = BNode()
            graph.add((subject, SKOSNO.isFromConceptIn, relation_node))
            graph.add((relation_node, RDF.type, SKOSNO.AssociativeConceptRelation))
            graph.add((relation_node, SKOSNO.hasToConcept, URIRef(relation["tilBegrep"])))
            language_literals(relation_node, SKOSNO.relationRole, relation["relasjonsrolle"])
    return graph


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data", type=Path, help="YAML instance data following begrepsmodell.yaml")
    parser.add_argument("-o", "--output", type=Path, help="Turtle file (default: stdout)")
    args = parser.parse_args()
    data = yaml.safe_load(args.data.read_text(encoding="utf-8"))
    turtle = to_rdf(data).serialize(format="turtle")
    if args.output:
        args.output.write_text(turtle, encoding="utf-8")
    else:
        sys.stdout.write(turtle)


if __name__ == "__main__":
    main()
