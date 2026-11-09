# /// script
# requires-python = ">=3.10"
# dependencies = ["linkml-runtime==1.9.5", "jinja2==3.1.6"]
# ///
"""Generate one Markdown class diagram for a complete LinkML schema."""

import argparse
from html import escape
from pathlib import Path
import sys

from jinja2 import Environment, FileSystemLoader, StrictUndefined
from linkml_runtime.utils.schemaview import SchemaView


def cardinality(slot):
    minimum = max(int(bool(slot.required or slot.identifier)), slot.minimum_cardinality or 0)
    maximum = slot.maximum_cardinality
    if not slot.multivalued:
        maximum = min(1, maximum) if maximum is not None else 1
    if maximum == minimum:
        return str(minimum)
    return f"{minimum}..{maximum if maximum is not None else '*'}"


def render_diagram(schema, *, exclude_attributes=False):
    view = SchemaView(str(schema))
    definitions = view.all_classes()
    ids = {name: f"c{index}" for index, name in enumerate(sorted(definitions))}
    classes, inheritance, relations = [], [], []
    for name in ids:
        definition = definitions[name]
        attributes = []
        for slot in sorted(view.class_induced_slots(name), key=lambda slot: slot.name):
            if slot.range in definitions:
                relations.append({
                    "source": ids[name],
                    "target": ids[slot.range],
                    "name": slot.name,
                    "cardinality": cardinality(slot),
                })
            elif not exclude_attributes:
                attributes.append({
                    "name": slot.name,
                    "range": slot.range or view.schema.default_range or "string",
                    "cardinality": cardinality(slot),
                })
        classes.append({
            "id": ids[name],
            "name": name,
            "abstract": bool(definition.abstract),
            "attributes": attributes,
        })
        if definition.is_a:
            inheritance.append({"parent": ids[definition.is_a], "child": ids[name]})

    environment = Environment(
        loader=FileSystemLoader(Path(__file__).parent / "templates"),
        undefined=StrictUndefined,
        trim_blocks=True,
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    environment.filters["label"] = lambda value: escape(str(value), quote=True).replace("\n", " ")
    return environment.get_template("class_diagram.md.jinja2").render(
        title=view.schema.title or view.schema.name,
        classes=classes,
        inheritance=inheritance,
        relations=relations,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("schema", type=Path, help="LinkML YAML file")
    parser.add_argument("-o", "--output", type=Path, help="Markdown file (default: stdout)")
    parser.add_argument("--exclude-attributes", action="store_true", help="Show classes and relations without fields")
    args = parser.parse_args()
    markdown = render_diagram(args.schema, exclude_attributes=args.exclude_attributes)
    if args.output:
        args.output.write_text(markdown, encoding="utf-8")
    else:
        sys.stdout.write(markdown)


if __name__ == "__main__":
    main()
