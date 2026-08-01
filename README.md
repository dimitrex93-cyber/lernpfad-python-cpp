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
| 01 | [Grundlagen der IT und erste Programme](lernfeld_01_grundlagen/) | Variablen, Datentypen, Ein-/Ausgabe, Kontrollstrukturen, Funktionen | Anfänger | ✅ komplett + Test |
| 02 | [Einfache Datenverarbeitung und Algorithmen](lernfeld_02_datenverarbeitung/) | Listen, Strings, Sortieren, Suchen, Komplexität, Dateien | Anfänger → Junior | ✅ Aufgaben + Test |
| 03 | [Objektorientierte Programmierung](lernfeld_03_oop/) | Klassen, Vererbung, Polymorphie, Kapselung | Junior | ✅ Aufgaben + Test |
| 04 | [Datenbanken und Schnittstellen](lernfeld_04_datenbanken/) | SQL, SQLite, JSON, REST-APIs | Junior → Mid-Level | ✅ Aufgaben + Test |
| 05 | [Komplexe Systeme und Netzwerke](lernfeld_05_netzwerke/) | Sockets, Webserver, Nebenläufigkeit, Protokolle | Mid-Level | ✅ Aufgaben + Test |
| 06 | [Softwarequalität, Testing und Projektmanagement](lernfeld_06_qualitaet/) | Tests, Debugging, Refactoring, Git, CI, Scrum | Mid-Level → Senior | ✅ Aufgaben + Test |

Die komplette Lernreise inkl. Zeitplan und Meilensteinen findest du in der
[**ROADMAP.md**](ROADMAP.md). Wie der Kurs zum offiziellen Ausbildungsrahmenplan
passt und wo Schwerpunkte gesetzt werden, erklärt die [**LEHRPLAN.md**](LEHRPLAN.md).

## Struktur des Repositories

```
lernpfad-python-cpp/
├── README.md                  ← diese Datei
├── ROADMAP.md                 ← gesamter Lernpfad Junior → Senior
├── LEHRPLAN.md                ← Anbindung an den Ausbildungsrahmenplan
├── CONTRIBUTING.md            ← so kannst du mitwirken
├── LICENSE                    ← MIT
├── tools/
│   ├── quiz.py                ← interaktiver Wissenstest (Lern-App!)
│   └── README.md              ← Benutzung von quiz.py
└── lernfeld_XX_thema/
    ├── python/
    │   ├── theorie/           ← Theorie-README (nur Python)
    │   ├── aufgaben/          ← Übungsaufgaben (Python)
    │   └── loesungen/         ← Musterlösungen (Python)
    ├── cpp/
    │   ├── theorie/           ← Theorie-README (nur C++)
    │   ├── aufgaben/          ← Übungsaufgaben (C++)
    │   └── loesungen/         ← Musterlösungen (C++)
    ├── test/                  ← bewerteter Test: fragen.json, test.md, loesungen.md
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
7. **Testen**: Stelle dein Wissen mit dem bewerteten Test des Moduls unter Beweis
   (siehe unten) – bestanden ab Note 4.

## Tests & Punktebewertung (wie eine Lern-App)

Zu **jedem Lernfeld** gibt es zwei Prüfungsformen mit einheitlichem
Notenschlüssel (≥ 92 % = 1, ≥ 50 % = 4, < 30 % = 6):

1. **Interaktiver Wissenstest** – der Lern-App-Modus:
   `python3 tools/quiz.py 1` (bzw. 2–6) startet den Test des Lernfelds.
   Multiple-Choice- und offene Fragen mit Punkten, Sofort-Feedback und
   Erklärungen. Dein Fortschritt wird lokal gespeichert
   (`~/.lernpfad/fortschritt.json`), Übersicht mit `python3 tools/quiz.py --status`.
2. **Schriftliche Klausur** – `lernfeld_XX/test/test.md` mit Aufgaben,
   Punktverteilung und Zeitlimit; der Lösungsbogen liegt in `test/loesungen.md`.

**Warum beides?** Der Quiz-Runner motiviert und zeigt Lücken sofort – wie bei
Sololearn oder Mimo. Die Klausur trainiert das, was in Prüfung und Beruf zählt:
Wissen aus dem Kopf formulieren, Code lesen und verstehen, Transfer leisten.
Details: [tools/README.md](tools/README.md) und [LEHRPLAN.md](LEHRPLAN.md).

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
- **Jedes Modul endet mit einem bewerteten Test** – nur wer besteht, ist bereit
  für das nächste Lernfeld.

## Mitwirken

Dieses Projekt lebt von der Community: Fehler korrigieren, Aufgaben verbessern,
Lösungen ergänzen, neue Module beisteuern. Wie das geht, steht in der
[**CONTRIBUTING.md**](CONTRIBUTING.md).

## Lizenz

[MIT](LICENSE) – frei nutzbar, veränderbar und weiterverteilbar.
