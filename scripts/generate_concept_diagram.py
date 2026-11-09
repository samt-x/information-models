# /// script
# requires-python = ">=3.10"
# dependencies = ["rdflib==7.4.0"]
# ///
"""Generate one Mermaid concept diagram directly from RDF Turtle."""

import argparse
from html import escape
from pathlib import Path
import sys
from textwrap import wrap

from rdflib import Graph, Literal, Namespace
from rdflib.namespace import DCTERMS, RDF, SKOS

SKOSNO = Namespace("https://data.norge.no/vocabulary/skosno#")
XKOS = Namespace("http://rdf-vocabulary.ddialliance.org/xkos#")


def label(text):
    return "<br/>".join(escape(line, quote=True) for line in wrap(text, width=28))


def render_diagram(graph, *, language="nb"):
    concepts = sorted(set(graph.subjects(RDF.type, SKOS.Concept)), key=str)
    if not concepts:
        raise ValueError("Turtle-filen inneholder ingen skos:Concept.")
    ids = {concept: f"n{index}" for index, concept in enumerate(concepts)}

    def text(subject, predicate, fallback):
        values = sorted((value for value in graph.objects(subject, predicate)
                         if isinstance(value, Literal)), key=lambda value: (value.language or "", str(value)))
        for lang in (language, "nb", None):
            for value in values:
                if value.language == lang:
                    return str(value)
        return str(values[0]) if values else fallback

    parents = set(graph.subject_objects(XKOS.specializes))
    parents.update((child, parent) for parent, child in graph.subject_objects(XKOS.generalizes))
    associations = set()
    for source, relation in graph.subject_objects(SKOSNO.isFromConceptIn):
        targets = list(graph.objects(relation, SKOSNO.hasToConcept))
        if not targets:
            raise ValueError(f"Assosiativ relasjon fra {source} mangler skosno:hasToConcept.")
        for target in targets:
            associations.add((source, target, text(relation, SKOSNO.relationRole, "relatert til")))
    for source, target in parents | {(source, target) for source, target, _ in associations}:
        for concept in (source, target):
            if concept not in ids:
                raise ValueError(f"Relasjonen viser til et begrep uten skos:Concept i filen: {concept}")

    collections = sorted(set(graph.subjects(RDF.type, SKOS.Collection)), key=str)
    title = text(collections[0], DCTERMS.title, "Begrepsdiagram") if collections else "Begrepsdiagram"
    lines = [
        f"# {title}",
        "",
        "Heltrukne piler peker fra underbegrep til overbegrep (`xkos:specializes`).",
        "Stiplede piler viser assosiative relasjoner med rollen fra dataene.",
        "",
        "```mermaid",
        "flowchart BT",
    ]
    for concept in concepts:
        name = text(concept, SKOS.prefLabel, str(concept))
        lines.append(f'    {ids[concept]}["{label(name)}"]')
    lines.append("")
    for source, target in sorted(parents, key=lambda pair: tuple(map(str, pair))):
        lines.append(f'    {ids[source]} -->|"spesialiserer"| {ids[target]}')
    for source, target, role in sorted(associations, key=lambda relation: tuple(map(str, relation))):
        lines.append(f'    {ids[source]} -. "{label(role)}" .-> {ids[target]}')
    lines.extend([
        "```",
        "",
        "Boksene er begreper i samlingen. Generiske begrepsrelasjoner uttrykker",
        "ikke LinkML-arv eller krav til forekomster av skoler.",
        "",
    ])
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("data", type=Path, help="Turtle file with SKOS concepts")
    parser.add_argument("-o", "--output", type=Path, help="Markdown file (default: stdout)")
    parser.add_argument("--language", choices=("nb", "nn"), default="nb", help="Label language (default: nb; missing translations fall back to nb)")
    args = parser.parse_args()
    graph = Graph().parse(args.data, format="turtle")
    markdown = render_diagram(graph, language=args.language)
    if args.output:
        args.output.write_text(markdown, encoding="utf-8")
    else:
        sys.stdout.write(markdown)


if __name__ == "__main__":
    main()
