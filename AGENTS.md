# LinkML i information-models

Skriv skjemaene i `linkml/`. Felles klasser hører hjemme i [kjerne.yaml](linkml/kjerne.yaml). Domenemoduler som [opplaring.yaml](linkml/opplaring.yaml) importerer kjernen med `imports: [kjerne]` og gjenbruker klassene derfra.

## Klasser og attributter

- Bruk `PascalCase` for klasser og `camelCase` for attributter. I tekniske navn skrives æ som a, ø som o og å som a, også for store bokstaver. Bruk samme regel i filnavn og egne IRI-er. Eksempler er `opplaring`, `fodselsdato` og `pameldt`. Bruk vanlig norsk rettskriving i visningsteksten.
- Skriv klassefeltene i rekkefølgen `class_uri`, `title`, `description`, `annotations`. Deretter kommer eventuelle felt for arv og koblinger, og til slutt `attributes`. Utelat felt som mangler innhold.
- Definer egenskaper lokalt under klassens `attributes`. Skriv `slot_uri`, `title`, `description`, `annotations` først når de finnes. Sett deretter `range`, kardinalitet og eventuelle andre egenskaper.
- Bruk to mellomrom per innrykksnivå. Legg inn én tom linje etter `classes:`, mellom klassene, etter hver `attributes:` og mellom attributtene. Dette gjelder også før det første attributtet når klassen bare har ett.

Utdrag fra `Deltaker` som viser oppsettet:

```yaml
classes:

  Deltaker:
    class_uri: opplaring:Deltaker
    title: deltaker
    description: Rolle som en fysisk person har når den deltar i et pedagogisk tilbud.
    annotations:
      title_nn: deltakar
      title_en: participant
    is_a: Rolle
    slot_usage:
      erRolleFor:
        range: FysiskPerson
    attributes:

      oppnar:
        slot_uri: opplaring:oppnar
        title: oppnår
        description: Angir et resultat som en deltaker har oppnådd.
        annotations:
          title_en: achieves
        range: Resultat
        multivalued: true

      pameldt:
        slot_uri: opplaring:pameldt
        title: påmeldt
        description: Angir et pedagogisk tilbud som en deltaker er meldt på.
        annotations:
          title_en: enrolled in
        range: PedagogiskTilbud
        multivalued: true
```

## Språk og kildegrunnlag

- Bruk bokmål i `title` og `description`. Bevar oversettelsene som finnes i kilden under `annotations`, med `title_nn`, `title_en`, `description_nn` og `description_en`. Bruk `aliases` for alternative navn. Standard OWL-eksport i LinkML 1.9.5 skriver oversettelsesannotasjonene som egne predikater. Kontroller den genererte RDF-en hvis leveransen krever språkmerkede titler.
- Når modellen bygger på OWL og SHACL, oppgi kildefilene med versjon i en kommentar øverst. Hent klasse- og egenskaps-IRI-er fra ontologien og måltyper og kardinalitet fra strukturformene. Når LinkML krever prosentkoding av en IRI, bevar originalen i `annotations.source_iri`.
- Bruk `is_a` for arv og `slot_usage` når en underklasse snevrer inn et arvet attributt. Eksempelvis definerer `Rolle` attributtet `erRolleFor` én gang, og `Deltaker` presiserer måltypen til `FysiskPerson`.
- Bevar klassespesifikke måltyper selv om to attributter har samme `slot_uri`. For eksempel peker `Resultat.gjelder` til `PedagogiskTilbud` og `Dokumentasjon.gjelder` til `Deltaker`. Bevar også inverse relasjoner når kilden angir dem.
- Når strukturformen tillater null eller flere verdier, bruk `multivalued: true` og la attributtet være valgfritt. Sett strengere grenser når de er angitt i kilden eller profilen.
