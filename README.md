# Information Models

## Utforsk modellene

- [LinkML-dokumentasjon – klasser, felter og relasjoner](https://samt-x.github.io/information-models/linkml/)
- [Ontology Explorer – utforsk TTL-modellene](https://samt-x.github.io/information-models/)

## Eksempelmodeller

### LinkML

[Oppvekst og læring – tre lag](models/eksempel/linkml/README.md)

[Domenemodell – med felter](models/eksempel/linkml/domenemodell.md)

```bash
uv run scripts/generate_domain_diagrams.py models/eksempel/linkml/domenemodell.yaml \
  --output models/eksempel/linkml/domenemodell.md
```

### SKOS-AP-NO

[Konseptuell modell – begrepsdiagram](models/eksempel/skos/konseptuell-modell.skos.md)

```bash
uv run scripts/generate_concept_diagram.py models/eksempel/skos/konseptuell-modell.skos.ttl \
  --output models/eksempel/skos/konseptuell-modell.skos.md
```
