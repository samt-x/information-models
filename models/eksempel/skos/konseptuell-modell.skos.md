# Begreper i skoledomenet

Heltrukne piler peker fra underbegrep til overbegrep (`xkos:specializes`).
Stiplede piler viser assosiative relasjoner med rollen fra dataene.

```mermaid
flowchart BT
    n0["elev"]
    n1["fylkeskommune"]
    n2["kommune"]
    n3["organisasjon"]
    n4["person"]
    n5["skole"]
    n6["ungdomsskole"]
    n7["videregående skole"]

    n0 -->|"spesialiserer"| n4
    n1 -->|"spesialiserer"| n3
    n2 -->|"spesialiserer"| n3
    n5 -->|"spesialiserer"| n3
    n6 -->|"spesialiserer"| n5
    n7 -->|"spesialiserer"| n5
    n0 -. "går på" .-> n5
    n5 -. "har skoleeier" .-> n3
    n6 -. "har skoleeier" .-> n2
    n7 -. "har skoleeier" .-> n1
```

Boksene er begreper i samlingen. Generiske begrepsrelasjoner uttrykker
ikke LinkML-arv eller krav til forekomster av skoler.
