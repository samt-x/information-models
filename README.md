# Information Models

## Eksempelmodeller

### LinkML

[Domenemodell – klassediagram](models/eksempel/linkml/domenemodell.md)

```bash
uv run scripts/generate_class_diagram.py models/eksempel/linkml/domenemodell.yaml \
  --exclude-attributes \
  --output models/eksempel/linkml/domenemodell.md
```

### SKOS-AP-NO

[Konseptuell modell – begrepsdiagram](models/eksempel/skos/konseptuell-modell.skos.md)

```bash
uv run scripts/generate_concept_diagram.py models/eksempel/skos/konseptuell-modell.skos.ttl \
  --output models/eksempel/skos/konseptuell-modell.skos.md
```
