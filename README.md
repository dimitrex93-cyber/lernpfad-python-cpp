# Lernpfad Python & C++ – Vom Programmieranfänger zum Senior-Entwickler

Ein **offener, strukturierter Selbstlernkurs** für alle, die Programmieren von Grund auf lernen
wollen – oder ihre Kenntnisse systematisch bis auf Senior-Niveau ausbauen möchten.

Der Kurs orientiert sich am **Ausbildungsrahmenplan für Fachinformatiker (Anwendungsentwicklung)**
und vermittelt jeden Lernstoff in **zwei Sprachen parallel**: **Python** (dynamisch, interpretiert)
und **C/C++** (statisch, kompiliert). So versteht man nicht nur *eine* Sprache, sondern die
**Konzepte dahinter** – und die Stärken und Schwächen beider Welten.

> 🎯 Zielgruppe: Programmieranfänger\*innen, Fachinformatiker-Azubis, Quereinsteiger\*innen
> und alle, die ihren Lernfortschritt strukturiert dokumentieren wollen.

---

## Warum Python UND C++?

| | Python | C++ |
|---|---|---|
| **Paradigma** | interpretiert, dynamisch typisiert | kompiliert, statisch typisiert |
| **Einstieg** | sehr schnell erste Erfolge | mehr Grundlagenwissen nötig |
| **Einsatz** | Scripting, Datenanalyse, Web, KI | Systemprogrammierung, Games, Embedded |
| **Lerneffekt** | schnell Ergebnisse, klare Syntax | tiefes Verständnis für Speicher & Hardware |

Wer **beide** Sprachen lernt, versteht, *warum* Programmiersprachen so sind, wie sie sind –
und kann später für jede Aufgabe die richtige Sprache wählen.

## Die 6 Lernfelder

| # | Lernfeld | Themen | Niveau | Status |
|---|---|---|---|---|
| 01 | [Grundlagen der IT und erste Programme](lernfeld_01_grundlagen/) | Variablen, Datentypen, Ein-/Ausgabe, Kontrollstrukturen, Funktionen | Anfänger | ✅ fertig |
| 02 | [Einfache Datenverarbeitung und Algorithmen](lernfeld_02_datenverarbeitung/) | Listen, Strings, Sortieren, Suchen, Komplexität, Dateien | Anfänger → Junior | 🚧 in Arbeit |
| 03 | [Objektorientierte Programmierung](lernfeld_03_oop/) | Klassen, Vererbung, Polymorphie, Kapselung | Junior | 🚧 in Arbeit |
| 04 | [Datenbanken und Schnittstellen](lernfeld_04_datenbanken/) | SQL, SQLite, JSON, REST-APIs | Junior → Mid-Level | 🚧 in Arbeit |
| 05 | [Komplexe Systeme und Netzwerke](lernfeld_05_netzwerke/) | Sockets, Webserver, Nebenläufigkeit, Protokolle | Mid-Level | 🚧 in Arbeit |
| 06 | [Softwarequalität, Testing und Projektmanagement](lernfeld_06_qualitaet/) | Tests, Debugging, Refactoring, Git, CI, Scrum | Mid-Level → Senior | 🚧 in Arbeit |

Die komplette Lernreise inkl. Zeitplan und Meilensteinen findest du in der
[**ROADMAP.md**](ROADMAP.md).

## Struktur des Repositories

```
lernpfad-python-cpp/
├── README.md                  ← diese Datei
├── ROADMAP.md                 ← gesamter Lernpfad Junior → Senior
├── CONTRIBUTING.md            ← so kannst du mitwirken
├── LICENSE                    ← MIT
└── lernfeld_XX_thema/
    ├── python/
    │   ├── theorie/           ← Theorie-README (nur Python)
    │   ├── aufgaben/          ← Übungsaufgaben (Python)
    │   └── loesungen/         ← Musterlösungen (Python)
    ├── cpp/
    │   ├── theorie/           ← Theorie-README (nur C++)
    │   ├── aufgaben/          ← Übungsaufgaben (C++)
    │   └── loesungen/         ← Musterlösungen (C++)
    ├── checklist.md           ← Lernfortschritt zum Abhaken
    ├── vergleich.md           ← Python vs. C++ im direkten Vergleich
    └── mini_projekt/          ← Abschlussprojekt des Moduls
```

## So arbeitest du mit dem Kurs

1. **Theorie lesen**: Beginne mit `python/theorie/README.md` (schneller Einstieg),
   dann `cpp/theorie/README.md` (vertieft das Verständnis durch den Kontrast).
2. **Aufgabe lösen**: Bearbeite jede Aufgabe **zuerst in Python**, danach in C++.
   So siehst du hautnah, wie sich dieselbe Idee in beiden Welten anfühlt.
3. **Vergleichen**: Wirf erst danach einen Blick in `loesungen/`.
4. **Abhaken**: Setze in `checklist.md` einen Haken pro erledigtem Punkt.
5. **Vertiefen**: Lies am Modulende `vergleich.md` mit der Gegenüberstellung
   von Performance, Speicher und Lesbarkeit.
6. **Abschließen**: Baue das `mini_projekt/` – ganz ohne Lösung, du schaffst das!

## Voraussetzungen

- **Python 3.10+** – nur die Standardbibliothek, keine externen Pakete nötig
- **C++17-Compiler** – z. B. `g++` (Linux/macOS) oder MinGW (Windows)
- **Terminal** – der Kurs ist bewusst **GUI-frei**, alles läuft in der Kommandozeile
- **Git** (optional) – für die eigene Versionskontrolle des Lernfortschritts

### C++ kompilieren

```bash
# Jede Lösung kompiliert mit:
g++ -std=c++17 -Wall -Wextra aufgabe_01.cpp -o aufgabe_01
./aufgabe_01
```

### Python ausführen

```bash
python3 aufgabe_01.py
```

## Konventionen

- **Keine GUIs** – nur Terminal-Anwendungen. Du bist mit der Kommandozeile vertraut? Perfekt.
- **Deutsch** als Unterrichts- und Kommentarsprache – der Kurs richtet sich an
  deutschsprachige Lernende (Fachinformatiker-Ausbildung).
- **Aufgaben immer zuerst in Python, dann in C++** – das ist kein Zufall, sondern Methode.
- **Musterlösungen sind Vorschläge**, keine Dogmen – es gibt immer viele Wege.

## Mitwirken

Dieses Projekt lebt von der Community: Fehler korrigieren, Aufgaben verbessern,
Lösungen ergänzen, neue Module beisteuern. Wie das geht, steht in der
[**CONTRIBUTING.md**](CONTRIBUTING.md).

## Lizenz

[MIT](LICENSE) – frei nutzbar, veränderbar und weiterverteilbar.
