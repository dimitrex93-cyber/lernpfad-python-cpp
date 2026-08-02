// Aufgabe 5: Projektmanagement & Git-Workflow — Musterlösung (C++)
//
// Dies ist eine Prozess-Aufgabe: Du planst und simulierst ein Mini-Projekt
// (Notenspiegel-Tool aus Aufgabe 4) im Berufsalltag-Stil – mit Git, Issues,
// Pull Request, Code-Review und Scrum-Rollen.
//
// Damit die Musterlösung „ausführbar“ ist, setzt dieses Programm alle
// sieben Schritte automatisiert um: Es legt das Projekt `notenspiegel/` an,
// schreibt README, Issues, Sprint-Planung, PR-Unterlagen, Review und
// Retrospektive und führt den kompletten Git-Workflow (init → Commits →
// feature-Branch) wirklich aus. Der Notenspiegel-Code wird dabei mit
// `g++ -std=c++17 -Wall -Wextra` gebaut und ausgeführt.
//
// Kompilieren:  g++ -std=c++17 -Wall -Wextra aufgabe_05.cpp -o /tmp/a05
// Ausführen:    /tmp/a05                  # Projekt in ./notenspiegel anlegen
//               /tmp/a05 /tmp/projekt     # Zielordner selbst wählen
//
// Die sieben Schritte der Aufgabe:
//   Schritt 1: Projekt anlegen (git init, README.md mit Build-Befehlen)
//   Schritt 2: Backlog & Issues (docs/issues.md)
//   Schritt 3: Sprint-Planung (docs/sprint_planung.md, Blickwinkel PO/SM/Dev)
//   Schritt 4: Feature-Branch & Arbeit (mehrere sinnvolle Commits)
//   Schritt 5: Pull Request (docs/pull_request.md mit Terminal-Ausgabe)
//   Schritt 6: Code-Review (docs/review.md, mind. 3 Kommentare)
//   Schritt 7: Retrospektive (docs/retrospektive.md, mind. 3 Maßnahmen)

#include <cstdlib>      // std::system, std::exit
#include <filesystem>   // std::filesystem (C++17)
#include <fstream>      // std::ofstream, std::ifstream
#include <iostream>     // std::cout, std::cerr
#include <string>       // std::string

namespace fs = std::filesystem;

// ---------------------------------------------------------------------------
// Hilfsfunktionen
// ---------------------------------------------------------------------------

void schreibe_datei(const fs::path& pfad, const std::string& inhalt) {
    if (!pfad.parent_path().empty()) {
        fs::create_directories(pfad.parent_path());
    }
    std::ofstream datei(pfad);
    if (!datei) {
        std::cerr << "FEHLER: " << pfad << " konnte nicht geschrieben werden"
                  << std::endl;
        std::exit(1);
    }
    datei << inhalt;
    std::cout << "  ✓ " << pfad.string() << std::endl;
}

void git(const fs::path& projekt, const std::string& argumente) {
    const std::string befehl =
        "git -C '" + projekt.string() + "' " + argumente;
    std::cout << "  $ " << befehl << std::endl;
    if (std::system(befehl.c_str()) != 0) {
        std::cerr << "FEHLER bei: " << befehl << std::endl;
        std::exit(1);
    }
}

void ausfuehren(const fs::path& verzeichnis, const std::string& befehl) {
    const std::string voll = "cd '" + verzeichnis.string() + "' && " + befehl;
    std::cout << "  $ " << befehl << std::endl;
    if (std::system(voll.c_str()) != 0) {
        std::cerr << "FEHLER bei: " << voll << std::endl;
        std::exit(1);
    }
}

void git_config_sicherstellen(const fs::path& projekt) {
    // Lokale Git-Identität setzen, falls global keine existiert.
    const std::string prüfe =
        "git -C '" + projekt.string() + "' config --get user.name > /dev/null 2>&1";
    if (std::system(prüfe.c_str()) != 0) {
        git(projekt, "config user.name 'Lernpfad-Teilnehmer'");
        git(projekt, "config user.email 'teilnehmer@lernpfad.example'");
        std::cout << "  ✓ Lokale Git-Identität gesetzt (user.name / user.email)"
                  << std::endl;
    }
}

std::string lese_datei(const fs::path& pfad) {
    std::ifstream datei(pfad);
    std::string inhalt((std::istreambuf_iterator<char>(datei)),
                       std::istreambuf_iterator<char>());
    return inhalt;
}

// ---------------------------------------------------------------------------
// Dokumente des simulierten Projekts (Inhalte der Dateien)
// ---------------------------------------------------------------------------

const std::string README = R"MD(# Notenspiegel-Tool

**Projektname:** Notenspiegel-Tool
**Sprache:** C++17 (Standardbibliothek, keine externen Abhängigkeiten)

## Ziel

Das Tool liest eine Liste von Schulnoten und gibt einen Notenspiegel aus:
wie oft jede Note (1–6) vorkommt – inklusive deutschem Namen.

## Funktionen

- Notenspiegel ausgeben (Häufigkeit der Noten 1–6 mit deutschem Namen)
- Durchschnitt der Noten berechnen
- Beste Note ermitteln (kleinste Zahl)

## Build- und Startbefehle

```bash
g++ -std=c++17 -Wall -Wextra notenspiegel.cpp -o notenspiegel
./notenspiegel
```

Alternativ mit dem Makefile: `make && ./notenspiegel`
)MD";

const std::string GITIGNORE = "notenspiegel\n";  // kompiliertes Binary nicht committen

const std::string ISSUES = R"MD(# Backlog & Issues

## Issue #1: Notenspiegel ausgeben

- **Typ:** Feature
- **Priorität:** Hoch
- **Beschreibung:** Das Tool soll für eine gegebene Notenliste zählen, wie
  oft jede Note (1–6) vorkommt, und das Ergebnis mit deutschem Namen
  ausgeben („sehr gut“, „gut“, …).
- **Akzeptanzkriterien:**
  - [ ] Die Ausgabe enthält alle sechs Noten mit Namen und Anzahl
  - [ ] Die Ausgabe ist stabil formatiert (Schleife, keine sechs Zeilen)

## Issue #2: Noten-Eingabe validieren

- **Typ:** Bugfix / Härtung
- **Priorität:** Mittel
- **Beschreibung:** Ungültige Eingaben (leere Liste, Noten außerhalb 1–6)
  dürfen das Programm nicht zum Absturz bringen.
- **Akzeptanzkriterien:**
  - [ ] Leere Liste führt zu einem verständlichen Fehler
        (`std::invalid_argument`)
  - [ ] Noten außerhalb 1–6 führen zu einem verständlichen Fehler

## Issue #3: Durchschnitt berechnen

- **Typ:** Feature
- **Priorität:** Mittel
- **Beschreibung:** Zusätzlich zum Notenspiegel soll der Durchschnitt der
  Noten ausgegeben werden.
- **Akzeptanzkriterien:**
  - [ ] `noten = {3, 1, 2, 1, 4, 5, 2, 3, 6}` ergibt Durchschnitt 3
  - [ ] Das Ergebnis ist eine Gleitkommazahl

## Issue #4: Beste Note ermitteln

- **Typ:** Feature
- **Priorität:** Niedrig
- **Beschreibung:** Die beste Note (kleinste Zahl) soll mit ausgegeben
  werden.
- **Akzeptanzkriterien:**
  - [ ] Bei `{2, 3, 1, 4}` wird 1 als beste Note gemeldet
)MD";

const std::string SPRINT_PLANUNG = R"MD(# Sprint-Planung (Sprint 1)

## Sprint-Ziel

„Ein lauffähiges Notenspiegel-Tool, das den Notenspiegel, den Durchschnitt
und die beste Note korrekt ausgibt und dabei ungültige Eingaben sauber
behandelt – gebaut mit `g++ -std=c++17 -Wall -Wextra` (null Warnungen).“

## Priorisiertes Backlog (ausgewählt vom Product Owner)

| Rang | Issue | Priorität | Aufwand (Dev) |
|------|-------|-----------|----------------|
| 1    | #1 Notenspiegel ausgeben | Hoch | klein |
| 2    | #2 Noten-Eingabe validieren | Mittel | klein |
| 3    | #3 Durchschnitt berechnen | Mittel | klein |
| 4    | #4 Beste Note ermitteln | Niedrig | klein |

## Blickwinkel der Rollen

- **Product Owner:** „Der Notenspiegel ist das Kern-Feature – ohne ihn gibt
  es kein Produkt. Validierung und Durchschnitt sichern die Qualität und
  gehören deshalb in den ersten Sprint. Die beste Note ist Nice-to-have,
  wird aber mitgenommen, weil sie fast nichts kostet.“
- **Scrum Master:** „Risiken: Git-Konflikte bei mehreren Commits, unklare
  Ausgabe-Formatierung, vergessene Randfall-Tests. Maßnahmen: kleine
  Commits mit klaren Meldungen, Referenz-Ausgabe notieren, Definition of
  Done festlegen (Code baut mit 0 Warnungen, Randfälle getestet, README
  aktuell).“
- **Dev-Team:** „Alle vier Issues sind klein (jeweils wenige Zeilen). Ich
  setze zuerst die Zähl-Logik um (Issue #1), sichere sie mit der
  Validierung ab (#2) und ergänze dann die beiden Ausgabe-Features (#3,
  #4). Nach jedem Commit: neu kompilieren und Ausgabe prüfen.“

## Definition of Done (DoD)

- [ ] Kompiliert mit `-std=c++17 -Wall -Wextra` ohne Warnungen
- [ ] Code läuft fehlerfrei durch
- [ ] Randfälle (leere Liste, ungültige Noten) getestet
- [ ] README aktuell, Commit vorhanden
)MD";

const std::string NOTENSPIEGEL_V1 = R"CPP(// Notenspiegel-Tool – zeigt, wie oft jede Note vorkommt.
#include <iostream>
#include <map>
#include <string>
#include <vector>

constexpr int MAX_NOTE = 6;

const std::map<int, std::string> NOTE_NAMEN = {
    {1, "sehr gut"}, {2, "gut"}, {3, "befriedigend"},
    {4, "ausreichend"}, {5, "mangelhaft"}, {6, "ungenügend"},
};

int zaehle_note(const std::vector<int>& noten, int note) {
    int anzahl = 0;
    for (int n : noten) {
        if (n == note) anzahl++;
    }
    return anzahl;
}

std::string note_zu_name(int note) {
    auto eintrag = NOTE_NAMEN.find(note);
    if (eintrag != NOTE_NAMEN.end()) return eintrag->second;
    return "ungültig";
}

void zeige_notenspiegel(const std::vector<int>& noten) {
    std::cout << "Notenspiegel:" << std::endl;
    for (int note = 1; note <= MAX_NOTE; note++) {
        std::cout << "Note " << note << " (" << note_zu_name(note) << "): "
                  << zaehle_note(noten, note) << std::endl;
    }
}

int main() {
    const std::vector<int> noten = {3, 1, 2, 1, 4, 5, 2, 3, 6};
    zeige_notenspiegel(noten);
    return 0;
}
)CPP";

const std::string NOTENSPIEGEL_V2 = R"CPP(// Notenspiegel-Tool – Notenspiegel, Durchschnitt und beste Note.
#include <iostream>
#include <map>
#include <stdexcept>
#include <string>
#include <vector>

constexpr int MAX_NOTE = 6;

const std::map<int, std::string> NOTE_NAMEN = {
    {1, "sehr gut"}, {2, "gut"}, {3, "befriedigend"},
    {4, "ausreichend"}, {5, "mangelhaft"}, {6, "ungenügend"},
};

int zaehle_note(const std::vector<int>& noten, int note) {
    int anzahl = 0;
    for (int n : noten) {
        if (n == note) anzahl++;
    }
    return anzahl;
}

double durchschnitt(const std::vector<int>& noten) {
    if (noten.empty()) {
        throw std::invalid_argument("Notenliste darf nicht leer sein");
    }
    double summe = 0.0;
    for (int note : noten) summe += note;
    return summe / static_cast<double>(noten.size());
}

int beste_note(const std::vector<int>& noten) {
    if (noten.empty()) {
        throw std::invalid_argument("Notenliste darf nicht leer sein");
    }
    int beste = noten[0];
    for (size_t i = 1; i < noten.size(); i++) {
        if (noten[i] < beste) beste = noten[i];
    }
    return beste;
}

std::string note_zu_name(int note) {
    auto eintrag = NOTE_NAMEN.find(note);
    if (eintrag != NOTE_NAMEN.end()) return eintrag->second;
    return "ungültig";
}

void zeige_notenspiegel(const std::vector<int>& noten) {
    std::cout << "Notenspiegel:" << std::endl;
    for (int note = 1; note <= MAX_NOTE; note++) {
        std::cout << "Note " << note << " (" << note_zu_name(note) << "): "
                  << zaehle_note(noten, note) << std::endl;
    }
    std::cout << "Durchschnitt: " << durchschnitt(noten) << std::endl;
    std::cout << "Beste Note: " << beste_note(noten) << std::endl;
}

int main() {
    const std::vector<int> noten = {3, 1, 2, 1, 4, 5, 2, 3, 6};
    zeige_notenspiegel(noten);
    return 0;
}
)CPP";

const std::string MAKEFILE =
    "CXX      = g++\n"
    "CXXFLAGS = -std=c++17 -Wall -Wextra\n"
    "\n"
    "notenspiegel: notenspiegel.cpp\n"
    "\t$(CXX) $(CXXFLAGS) notenspiegel.cpp -o notenspiegel\n"
    "\n"
    "clean:\n"
    "\trm -f notenspiegel\n";

std::string pull_request_dokument(const std::string& ausgabe) {
    // Füllt die PR-Vorlage aus der Aufgabe mit echten Werten.
    return R"MD(# Pull Request: Notenspiegel-Tool

**Branch:** feature/notenspiegel → main
**Behebt Issues:** #1, #2, #3, #4

## Beschreibung

Dieser PR bringt das Notenspiegel-Tool auf den Stand von Sprint 1: Der
Notenspiegel (Issue #1) wird ausgegeben, Eingaben werden validiert (Issue
#2) und zusätzlich werden Durchschnitt (Issue #3) sowie beste Note (Issue
#4) berechnet. Der Code ist das Ergebnis des Refactorings aus Lernfeld 6,
Aufgabe 4.

## Änderungen

- `notenspiegel.cpp`: Zähl-Logik (eine parametrisierte Funktion statt
  sechs Duplikaten), `std::map` NOTE_NAMEN, Validierung, Durchschnitt und
  beste Note
- `Makefile`: Build-Einzeiler (`make`)
- `README.md`: Projektbeschreibung und Build-/Startbefehle
- `docs/issues.md`, `docs/sprint_planung.md`: Backlog und Sprint-Planung

## Getestet

- [x] `g++ -std=c++17 -Wall -Wextra notenspiegel.cpp -o notenspiegel`
      → kompiliert ohne Warnungen
- [x] `./notenspiegel` liefert korrekte Ausgabe
- [x] Randfall: leere Liste wirft `std::invalid_argument` (kein Absturz)

## Ausgabe

```text
)MD"
    // Terminal-Ausgabe des Tools als „Screenshot“ einbetten
    + ausgabe
    + "```\n"
    + R"MD(
## Checkliste

- [x] Code kommentiert, wo nötig
- [x] Keine Debug-Ausgaben
- [x] README aktualisiert
)MD";
}

const std::string REVIEW = R"MD(# Code-Review: `noten_utils.cpp` (PR eines Kollegen)

Review-Regeln: Kommentare mit Datei und Zeile, Problem benennen, konkreten
Vorschlag machen – sachlich bleiben (Code reviewen, nicht die Person).

```cpp
#include <iostream>                                       // Zeile 1
#include <vector>                                         // Zeile 2
                                                          // Zeile 3
double durchschnitt(const std::vector<double>& noten) {   // Zeile 4
    double summe = 0;                                     // Zeile 5
    for (double note : noten) {                           // Zeile 6
        summe += note;                                    // Zeile 7
    }                                                     // Zeile 8
    return summe / noten.size();                          // Zeile 9
}                                                         // Zeile 10
                                                          // Zeile 11
int main() {                                              // Zeile 12
    std::vector<double> noten = {2, 4, 1, 3};             // Zeile 13
    std::cout << "Durchschnitt: " << durchschnitt(noten) << std::endl;   // Zeile 14
    std::cout << "Notenanzahl: " << noten.size() << std::endl;           // Zeile 15
    return 0;                                             // Zeile 16
}                                                         // Zeile 17
```

## Kommentare

| Datei | Zeile | Problem | Vorschlag |
|-------|-------|---------|-----------|
| `noten_utils.cpp` | 9 | Bei leerer Liste ist `noten.size()` = 0 → Division durch 0 (Ergebnis `nan`) | Leere Liste vor der Rechnung prüfen und `std::invalid_argument` mit verständlicher Meldung werfen |
| `noten_utils.cpp` | 6 | `note` wird pro Schleifendurchlauf kopiert (unnötig bei `double`) | `for (const auto& note : noten)` – zeigt die Lese-Absicht und vermeidet Kopien |
| `noten_utils.cpp` | 14–15 | `std::endl` schreibt zusätzlich einen Flush – in Schleifen/Logs unnötig langsam | `'\n'` verwenden, nur bei echter Flush-Notwendigkeit `std::endl` |
| `noten_utils.cpp` | 4–10 | Noten werden nicht validiert – Werte außerhalb 1–6 fließen ungeprüft in den Durchschnitt | Gültigkeit prüfen (1.0–6.0) und bei Verstoß einen Fehler melden |

*(Die ersten beiden Kommentare sind aus dem Aufgabenbeispiel, die letzten
beiden sind selbst ergänzt – insgesamt 4.)*
)MD";

const std::string RETROSPEKTIVE = R"MD(# Retrospektive Sprint 1

## Was lief gut?

- TDD hat sich gelohnt: Die Tests aus Aufgabe 2 (doctest) haben das
  Refactoring in Aufgabe 4 abgesichert – kein Verhaltensbruch.
- `-Wall -Wextra` mit null Warnungen fühlt sich gut an – der Compiler ist
  der erste Reviewer.
- Kleine, sinnvolle Commits machen die Historie lesbar
  (`git log --oneline`).

## Was lief schlecht?

- Die Sprint-Planung hat länger gedauert als der eigentliche Code –
  nächstes Mal Schätzungen konsequent kurz halten.
- Am Anfang fehlte eine klare Definition of Done; dadurch war unklar, wann
  ein Issue wirklich fertig ist.
- Das Makefile kam erst spät dazu – der Build war vorher ein
  Copy-and-Paste-Befehl.

## Maßnahmen für den nächsten Sprint (mindestens 3)

1. **DoD vor dem Sprint festlegen:** Jedes Issue bekommt vor der Arbeit
   explizite Akzeptanzkriterien, die auch wirklich abgehakt werden.
2. **Zeitbox für Schätzungen:** Aufwandsschätzung auf 10 Minuten begrenzen,
   dann entscheiden – Perfektionismus vermeiden.
3. **Build automatisieren:** Das Makefile gehört in den ersten Commit –
   `make && ./notenspiegel` ist der Standard-Workflow.
4. **CI-Gewohnheit:** Nach jedem Commit bauen und Tests ausführen – so
   bleibt der Branch immer grün.
)MD";

// ---------------------------------------------------------------------------
// Hauptprogramm – die 7 Schritte der Aufgabe
// ---------------------------------------------------------------------------

int main(int argc, char* argv[]) {
    fs::path projekt = (argc > 1) ? fs::path(argv[1])
                                  : fs::current_path() / "notenspiegel";
    projekt = fs::absolute(projekt);

    if (fs::exists(projekt) && !fs::is_empty(projekt)) {
        std::cerr << "FEHLER: " << projekt
                  << " existiert bereits und ist nicht leer. "
                     "Bitte leeren Zielordner wählen." << std::endl;
        return 1;
    }

    std::cout << "=== Schritt 1: Projekt anlegen (" << projekt.string() << ")"
              << std::endl;
    fs::create_directories(projekt);
    schreibe_datei(projekt / "README.md", README);
    schreibe_datei(projekt / ".gitignore", GITIGNORE);
    git(projekt, "init -b main");
    git_config_sicherstellen(projekt);
    git(projekt, "add README.md .gitignore");
    git(projekt, "commit -m 'Add README und .gitignore'");

    std::cout << "=== Schritt 2: Backlog & Issues ===" << std::endl;
    schreibe_datei(projekt / "docs" / "issues.md", ISSUES);
    git(projekt, "add docs/issues.md");
    git(projekt, "commit -m 'Add Issue-Backlog (docs/issues.md)'");

    std::cout << "=== Schritt 3: Sprint-Planung ===" << std::endl;
    schreibe_datei(projekt / "docs" / "sprint_planung.md", SPRINT_PLANUNG);
    git(projekt, "add docs/sprint_planung.md");
    git(projekt, "commit -m 'Add Sprint-Planung (docs/sprint_planung.md)'");

    std::cout << "=== Schritt 4: Feature-Branch & Arbeit ===" << std::endl;
    git(projekt, "checkout -b feature/notenspiegel");

    // Commit 1: Grundversion (Issue #1) – bauen und ausführen
    schreibe_datei(projekt / "notenspiegel.cpp", NOTENSPIEGEL_V1);
    ausfuehren(projekt, "g++ -std=c++17 -Wall -Wextra notenspiegel.cpp -o notenspiegel");
    ausfuehren(projekt, "./notenspiegel");
    git(projekt, "add notenspiegel.cpp");
    git(projekt, "commit -m 'Add Notenspiegel-Ausgabe (Issue #1)'");

    // Commit 2: Durchschnitt + beste Note (Issues #3, #4) – bauen, ausführen,
    // Terminal-Ausgabe für den PR erfassen
    schreibe_datei(projekt / "notenspiegel.cpp", NOTENSPIEGEL_V2);
    ausfuehren(projekt, "g++ -std=c++17 -Wall -Wextra notenspiegel.cpp -o notenspiegel");
    ausfuehren(projekt, "./notenspiegel > ausgabe.txt");
    git(projekt, "add notenspiegel.cpp");
    git(projekt, "commit -m 'Add Durchschnitt und beste Note (Issues #3, #4)'");

    std::cout << "=== Schritt 5: Pull Request ===" << std::endl;
    const std::string tool_ausgabe = lese_datei(projekt / "ausgabe.txt");
    fs::remove(projekt / "ausgabe.txt");  // temporäre Datei wieder aufräumen
    schreibe_datei(projekt / "docs" / "pull_request.md",
                   pull_request_dokument(tool_ausgabe));
    schreibe_datei(projekt / "Makefile", MAKEFILE);
    schreibe_datei(projekt / "docs" / "review.md", REVIEW);
    schreibe_datei(projekt / "docs" / "retrospektive.md", RETROSPEKTIVE);
    git(projekt, "add docs/pull_request.md Makefile docs/review.md docs/retrospektive.md");
    git(projekt, "commit -m 'Add Makefile, PR-Unterlagen, Review und Retrospektive'");

    std::cout << "=== Schritt 6 & 7 erledigt: Review und Retrospektive sind in docs/ ==="
              << std::endl;
    std::cout << "\n=== Ergebnis: Git-Historie ===" << std::endl;
    ausfuehren(projekt, "git log --oneline --all");
    std::cout << "=== Branches ===" << std::endl;
    ausfuehren(projekt, "git branch");
    std::cout << "Fertig! Projekt liegt unter: " << projekt.string() << std::endl;
    return 0;
}
