# Oppvekst og læring – informasjonsmodell i tre lag

<!-- Generert fra LinkML-kildene. Se README.md for kommando. -->

Klassene er gruppert etter LinkML-modul.
Stiplede piler peker fra underklasse til overklasse og betyr **arver fra**.
Heltrukne piler viser navngitte relasjoner med kardinalitet ved målet.
Arvede relasjoner vises bare på overklassen.

```mermaid
%%{init: {"flowchart": {"defaultRenderer": "dagre-wrapper"}}}%%
flowchart BT
    subgraph m0["Toppontologi"]
        c4["Fysisk person"]
        c10["Virksomhet"]
    end

    subgraph m1["Domenekjerne for oppvekst og læring"]
        c6["Oppvekstvirksomhet"]
        c9["Støtte- og hjelpevirksomhet"]
        c0["Ansatt"]
        c1["Deltaker"]
        c5["Omsorgsrolle"]
        c7["Pedagogisk tilbud"]
        c8["Resultat"]
        c2["Dokumentasjon"]
        c6 -->|"tilbyr · 0..*"| c7
        c9 -->|"støtter · 0..*"| c6
        c0 -->|"ansattVed · 0..*"| c6
        c0 -->|"utfører · 0..*"| c7
        c1 -->|"harOmsorgsrolle · 0..*"| c5
        c1 -->|"oppnår · 0..*"| c8
        c1 -->|"påmeldt · 0..*"| c7
        c5 -->|"erForesattFor · 0..*"| c1
        c7 -->|"tilbysAv · 0..*"| c6
        c8 -->|"dokumenteresGjennom · 0..*"| c2
        c8 -->|"gjelder · 0..*"| c7
        c2 -->|"gjelder · 0..*"| c1
    end

    subgraph m2["Underdomene for opplæring"]
        c3["Enkeltkarakter"]
        c11["Vitnemål"]
    end

    c0 -->|"erRolleFor · 1"| c4
    c1 -->|"erRolleFor · 1"| c4
    c5 -->|"erRolleFor · 1"| c4
    %% Lengre arvepiler gir plass til hver bane over den neste.
    c6 -...-> c10
    c9 -...-> c10
    c3 -...-> c8
    c11 -...-> c2

    style m0 fill:#e3f2fd,stroke:#1565c0,color:#111827
    style m1 fill:#e8f5e9,stroke:#2e7d32,color:#111827
    style m2 fill:#fff8e1,stroke:#a66b00,color:#111827
    classDef begrep fill:#ffffff,stroke:#475569,color:#111827
    class c4,c10,c6,c9,c0,c1,c5,c7,c8,c2,c3,c11 begrep
```

Diagrammet er generert fra LinkML-modellen og dens importerte moduler.
Banene bruker Mermaid-subgrafer med Dagre-layout og ekstra avstand mellom lagene.

## Klassediagrammer per domene

Hvert diagram viser alle klasser i domenet med egne og arvede datafelt.
Feltene viser datatype og kardinalitet. Relasjoner vises som navngitte piler
med kardinalitet, og trekantpiler peker mot overklassen.
Klasser merket «ekstern» tilhører et annet domene og vises uten felt.

### Toppontologi

```mermaid
classDiagram
    direction TB
    class c4["Fysisk person"] {
        string biologiskKjønn [0..1]
        string bostedsadresse [0..1]
        string etternavn [0..1]
        string folkeregistrertAdresse [0..1]
        string fornavn [0..1]
        string fulltNavn [0..1]
        date fødselsdato [0..1]
        string identifikasjonsnummer [0..1]
        string juridiskKjønn [0..1]
        string mellomnavn [0..1]
        string sivilstand [0..1]
        string statsborgerskap [0..*]
    }
    class c10["Virksomhet"] {
        string besøksadresse [0..1]
        string kontaktinformasjon [0..*]
        string navn [0..1]
        string næringskode [0..1]
        string organisasjonsform [0..1]
        string organisasjonsnummer [0..1]
        string postadresse [0..1]
    }


```

### Domenekjerne for oppvekst og læring

```mermaid
classDiagram
    direction TB
    class c0["Ansatt"] {
        string ansattnummer [0..1]
        string ansettelsestid [0..1]
        string stillingsbeskrivelse [0..1]
    }
    class c1["Deltaker"] {
        string deltakeridentifikator [0..1]
    }
    class c2["Dokumentasjon"] {
        string dokumentasjonIdentifikator [0..1]
        string dokumentnavn [0..1]
        string dokumentnummer [0..1]
        string dokumenttype [0..1]
        string status [0..1]
    }
    class c5["Omsorgsrolle"] {
    }
    class c6["Oppvekstvirksomhet"] {
        string besøksadresse [0..1]
        string geografi [0..1]
        string kontaktinformasjon [0..*]
        string navn [0..1]
        string næringskode [0..1]
        string oppvekstvirksomhetIdentifikasjon [0..*]
        string organisasjonsform [0..1]
        string organisasjonsnummer [0..1]
        string postadresse [0..1]
        string virksomhetstype [0..1]
    }
    class c7["Pedagogisk tilbud"] {
        string beskrivelse [0..1]
        string identifikator [0..1]
        string navnPåTilbud [0..1]
        string periode [0..1]
    }
    class c8["Resultat"] {
        string endeligResultat [0..1]
        string foreløpigResultat [0..1]
    }
    class c9["Støtte- og hjelpevirksomhet"] {
        string besøksadresse [0..1]
        string kontaktinformasjon [0..*]
        string navn [0..1]
        string næringskode [0..1]
        string organisasjonsform [0..1]
        string organisasjonsnummer [0..1]
        string postadresse [0..1]
        string typeStoetteOgHjelpevirksomhet [0..1]
    }
    class c4["Fysisk person"] {
        <<ekstern>>
    }
    class c10["Virksomhet"] {
        <<ekstern>>
    }

    c10 <|-- c6
    c10 <|-- c9

    c0 --> "0..*" c6 : ansattVed
    c0 --> "1" c4 : erRolleFor
    c0 --> "0..*" c7 : utfører
    c1 --> "1" c4 : erRolleFor
    c1 --> "0..*" c5 : harOmsorgsrolle
    c1 --> "0..*" c8 : oppnår
    c1 --> "0..*" c7 : påmeldt
    c2 --> "0..*" c1 : gjelder
    c5 --> "0..*" c1 : erForesattFor
    c5 --> "1" c4 : erRolleFor
    c6 --> "0..*" c7 : tilbyr
    c7 --> "0..*" c6 : tilbysAv
    c8 --> "0..*" c2 : dokumenteresGjennom
    c8 --> "0..*" c7 : gjelder
    c9 --> "0..*" c6 : støtter
```

### Underdomene for opplæring

```mermaid
classDiagram
    direction TB
    class c3["Enkeltkarakter"] {
        string endeligResultat [0..1]
        string foreløpigResultat [0..1]
    }
    class c11["Vitnemål"] {
        string dokumentasjonIdentifikator [0..1]
        string dokumentnavn [0..1]
        string dokumentnummer [0..1]
        string dokumenttype [0..1]
        string status [0..1]
    }
    class c1["Deltaker"] {
        <<ekstern>>
    }
    class c2["Dokumentasjon"] {
        <<ekstern>>
    }
    class c7["Pedagogisk tilbud"] {
        <<ekstern>>
    }
    class c8["Resultat"] {
        <<ekstern>>
    }

    c8 <|-- c3
    c2 <|-- c11

    c3 --> "0..*" c2 : dokumenteresGjennom
    c3 --> "0..*" c7 : gjelder
    c11 --> "0..*" c1 : gjelder
```
