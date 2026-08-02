"""Aufgabe 5: Projektmanagement & Git-Workflow — Musterlösung (Python).

Dies ist eine Prozess-Aufgabe: Du planst und simulierst ein Mini-Projekt
(Notenspiegel-Tool aus Aufgabe 4) im Berufsalltag-Stil – mit Git, Issues,
Pull Request, Code-Review und Scrum-Rollen.

Damit die Musterlösung „ausführbar“ ist, setzt dieses Skript alle sieben
Schritte automatisiert um: Es legt das Projekt `notenspiegel/` an, schreibt
README, Issues, Sprint-Planung, PR-Unterlagen, Review und Retrospektive und
führt den kompletten Git-Workflow (init → Commits → feature-Branch) wirklich
aus. Die Git-Befehle findest du am Ende zusätzlich als Zusammenfassung.

Aufruf:
    python3 aufgabe_05.py                 # Projekt in ./notenspiegel anlegen
    python3 aufgabe_05.py /tmp/projekt    # Zielordner selbst wählen

Die sieben Schritte der Aufgabe:
    Schritt 1: Projekt anlegen (git init, README.md)
    Schritt 2: Backlog & Issues (docs/issues.md)
    Schritt 3: Sprint-Planung (docs/sprint_planung.md, Blickwinkel PO/SM/Dev)
    Schritt 4: Feature-Branch & Arbeit (mehrere sinnvolle Commits)
    Schritt 5: Pull Request (docs/pull_request.md mit Terminal-Ausgabe)
    Schritt 6: Code-Review (docs/review.md, mind. 3 Kommentare)
    Schritt 7: Retrospektive (docs/retrospektive.md, mind. 3 Maßnahmen)
"""

from pathlib import Path
import subprocess
import sys


# ---------------------------------------------------------------------------
# Hilfsfunktionen
# ---------------------------------------------------------------------------

def git(projekt: Path, *argumente: str) -> subprocess.CompletedProcess:
    """Führt einen Git-Befehl im Projektordner aus."""
    ergebnis = subprocess.run(
        ["git", "-C", str(projekt), *argumente],
        capture_output=True,
        text=True,
    )
    if ergebnis.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(argumente)} fehlgeschlagen: {ergebnis.stderr.strip()}"
        )
    return ergebnis


def schreibe_datei(pfad: Path, inhalt: str) -> None:
    """Schreibt eine Textdatei (erzeugt den Ordner bei Bedarf)."""
    pfad.parent.mkdir(parents=True, exist_ok=True)
    pfad.write_text(inhalt, encoding="utf-8")
    print(f"  ✓ {pfad.relative_to(projekt)}")


def git_config_sicherstellen(projekt: Path) -> None:
    """Setzt eine lokale Git-Identität, falls global keine existiert."""
    if subprocess.run(
        ["git", "-C", str(projekt), "config", "--get", "user.name"],
        capture_output=True,
    ).returncode != 0:
        git(projekt, "config", "user.name", "Lernpfad-Teilnehmer")
        git(projekt, "config", "user.email", "teilnehmer@lernpfad.example")
        print("  ✓ Lokale Git-Identität gesetzt (user.name / user.email)")


# ---------------------------------------------------------------------------
# Datei-Inhalte (Dokumente des simulierten Projekts)
# ---------------------------------------------------------------------------

README = """# Notenspiegel-Tool

**Projektname:** Notenspiegel-Tool
**Sprache:** Python 3 (Standardbibliothek, keine externen Abhängigkeiten)

## Ziel

Das Tool liest eine Liste von Schulnoten und gibt einen Notenspiegel aus:
wie oft jede Note (1–6) vorkommt – inklusive deutschem Namen.

## Funktionen

- Notenspiegel ausgeben (Häufigkeit der Noten 1–6 mit deutschem Namen)
- Durchschnitt der Noten berechnen
- Beste Note ermitteln (kleinste Zahl)

## Bedienung

```bash
python3 notenspiegel.py        # Tool starten
python3 -m unittest            # Tests ausführen (falls vorhanden)
```
"""

ISSUES = """# Backlog & Issues

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
  - [ ] Leere Liste führt zu einem verständlichen Fehler (ValueError)
  - [ ] Noten außerhalb 1–6 führen zu einem verständlichen Fehler

## Issue #3: Durchschnitt berechnen

- **Typ:** Feature
- **Priorität:** Mittel
- **Beschreibung:** Zusätzlich zum Notenspiegel soll der Durchschnitt der
  Noten ausgegeben werden.
- **Akzeptanzkriterien:**
  - [ ] `noten = [3, 1, 2, 1, 4, 5, 2, 3, 6]` ergibt Durchschnitt 3.0
  - [ ] Das Ergebnis ist eine Gleitkommazahl

## Issue #4: Beste Note ermitteln

- **Typ:** Feature
- **Priorität:** Niedrig
- **Beschreibung:** Die beste Note (kleinste Zahl) soll mit ausgegeben
  werden.
- **Akzeptanzkriterien:**
  - [ ] Bei `[2, 3, 1, 4]` wird 1 als beste Note gemeldet
"""

SPRINT_PLANUNG = """# Sprint-Planung (Sprint 1)

## Sprint-Ziel

„Ein lauffähiges Notenspiegel-Tool, das den Notenspiegel, den Durchschnitt
und die beste Note korrekt ausgibt und dabei ungültige Eingaben sauber
behandelt.“

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
  Done festlegen (Code läuft, Randfälle getestet, README aktuell).“
- **Dev-Team:** „Alle vier Issues sind klein (jeweils wenige Zeilen). Ich
  setze zuerst die Zähl-Logik um (Issue #1), sichere sie mit der
  Validierung ab (#2) und ergänze dann die beiden Ausgabe-Features (#3,
  #4). Nach jedem Commit: `python3 notenspiegel.py` ausführen und Ausgabe
  prüfen.“

## Definition of Done (DoD)

- [ ] Code läuft fehlerfrei durch
- [ ] Randfälle (leere Liste, ungültige Noten) getestet
- [ ] README aktuell
- [ ] Commit gepusht / Commits vorhanden
"""

NOTENSPIEGEL_V1 = '''"""Notenspiegel-Tool – zeigt, wie oft jede Note vorkommt."""

NOTE_NAMEN = {
    1: "sehr gut",
    2: "gut",
    3: "befriedigend",
    4: "ausreichend",
    5: "mangelhaft",
    6: "ungenügend",
}

MAX_NOTE = 6


def zaehle_note(noten, note):
    """Zählt, wie oft `note` in der Liste `noten` vorkommt."""
    anzahl = 0
    for n in noten:
        if n == note:
            anzahl += 1
    return anzahl


def zeige_notenspiegel(noten):
    """Gibt den Notenspiegel formatiert aus."""
    print("Notenspiegel:")
    for note in range(1, MAX_NOTE + 1):
        name = NOTE_NAMEN.get(note, "ungültig")
        print(f"Note {note} ({name}): {zaehle_note(noten, note)}")


def main():
    noten = [3, 1, 2, 1, 4, 5, 2, 3, 6]
    zeige_notenspiegel(noten)


if __name__ == "__main__":
    main()
'''

NOTENSPIEGEL_V2 = '''"""Notenspiegel-Tool – Notenspiegel, Durchschnitt und beste Note."""

NOTE_NAMEN = {
    1: "sehr gut",
    2: "gut",
    3: "befriedigend",
    4: "ausreichend",
    5: "mangelhaft",
    6: "ungenügend",
}

MAX_NOTE = 6


def zaehle_note(noten, note):
    """Zählt, wie oft `note` in der Liste `noten` vorkommt."""
    anzahl = 0
    for n in noten:
        if n == note:
            anzahl += 1
    return anzahl


def durchschnitt(noten):
    """Liefert den Durchschnitt der Noten (leere Liste → ValueError)."""
    if not noten:
        raise ValueError("Notenliste darf nicht leer sein")
    return sum(noten) / len(noten)


def beste_note(noten):
    """Liefert die beste Note = kleinste Zahl (leere Liste → ValueError)."""
    if not noten:
        raise ValueError("Notenliste darf nicht leer sein")
    return min(noten)


def zeige_notenspiegel(noten):
    """Gibt den Notenspiegel, Durchschnitt und beste Note aus."""
    print("Notenspiegel:")
    for note in range(1, MAX_NOTE + 1):
        name = NOTE_NAMEN.get(note, "ungültig")
        print(f"Note {note} ({name}): {zaehle_note(noten, note)}")
    print("Durchschnitt:", durchschnitt(noten))
    print("Beste Note:", beste_note(noten))


def main():
    noten = [3, 1, 2, 1, 4, 5, 2, 3, 6]
    zeige_notenspiegel(noten)


if __name__ == "__main__":
    main()
'''


def pull_request_dokument(ausgabe: str) -> str:
    """Füllt die PR-Vorlage aus der Aufgabe mit echten Werten."""
    return f"""# Pull Request: Notenspiegel-Tool

**Branch:** feature/notenspiegel → main
**Behebt Issues:** #1, #2, #3, #4

## Beschreibung

Dieser PR bringt das Notenspiegel-Tool auf den Stand von Sprint 1: Der
Notenspiegel (Issue #1) wird ausgegeben, Eingaben werden validiert (Issue
#2) und zusätzlich werden Durchschnitt (Issue #3) sowie beste Note (Issue
#4) berechnet. Der Code ist das Ergebnis des Refactorings aus Lernfeld 6,
Aufgabe 4.

## Änderungen

- `notenspiegel.py`: Zähl-Logik (eine parametrisierte Funktion statt sechs
  Duplikaten), Dictionary `NOTE_NAMEN`, Validierung, Durchschnitt und
  beste Note
- `README.md`: Projektbeschreibung und Bedienung
- `docs/issues.md`, `docs/sprint_planung.md`: Backlog und Sprint-Planung

## Getestet

- [x] `python3 notenspiegel.py` liefert korrekte Ausgabe
- [x] Randfall: leere Liste wirft ValueError (stürzt nicht ab)
- [x] Randfall: eine einzelne Note funktioniert

## Ausgabe

```text
{ausgabe.rstrip()}
```

## Checkliste

- [x] Code kommentiert, wo nötig
- [x] Keine Debug-Ausgaben
- [x] README aktualisiert
"""

REVIEW = """# Code-Review: `noten_utils.py` (PR eines Kollegen)

Review-Regeln: Kommentare mit Datei und Zeile, Problem benennen, konkreten
Vorschlag machen – sachlich bleiben (Code reviewen, nicht die Person).

```python
def noten_durchschnitt(noten):          # Zeile 1
    summe = 0                           # Zeile 2
    for note in noten:                  # Zeile 3
        summe += note                   # Zeile 4
    return summe / len(noten)           # Zeile 5

def beste(noten):                       # Zeile 7
    beste = 6                           # Zeile 8
    for note in noten:                  # Zeile 9
        if note < beste:                # Zeile 10
            beste = note                # Zeile 11
    return beste                        # Zeile 12

noten = [2, 4, 1, 3]                    # Zeile 14
print("Durchschnitt:", noten_durchschnitt(noten))   # Zeile 15
print("Beste Note:", beste(noten))                  # Zeile 16
```

## Kommentare

| Datei | Zeile | Problem | Vorschlag |
|-------|-------|---------|-----------|
| `noten_utils.py` | 5 | Bei leerer Liste ist `len(noten)` = 0 → `ZeroDivisionError` (Absturz) | Leere Liste vor der Rechnung prüfen und `ValueError` mit verständlicher Meldung werfen |
| `noten_utils.py` | 7–12 | Name `beste` ist mehrdeutig („beste“ = kleinste Note?), und `6` ist eine magische Zahl | Umbenennen in `beste_note`, Startwert als Konstante `MAX_NOTE = 6` oder aus `noten[0]` ableiten |
| `noten_utils.py` | 1 | Kein Docstring, keine Typhinweise – Absicht der Funktion ist nicht erkennbar | `def notendurchschnitt(noten: list[float]) -> float:` plus ein Satz im Docstring |
| `noten_utils.py` | 14–16 | Modul-Level-Code: Die `print`-Aufrufe laufen schon beim Import der Datei (z. B. in Tests) | Code in `main()` verschieben und mit `if __name__ == "__main__":` schützen |
"""

RETROSPEKTIVE = """# Retrospektive Sprint 1

## Was lief gut?

- TDD hat sich gelohnt: Die Tests aus Aufgabe 2 haben das Refactoring in
  Aufgabe 4 abgesichert – kein Verhaltensbruch.
- Kleine, sinnvolle Commits machen die Historie lesbar
  (`git log --oneline`).
- Die Dokumentation (README, Issues, PR-Vorlage) war schneller fertig als
  erwartet.

## Was lief schlecht?

- Die Sprint-Planung hat länger gedauert als der eigentliche Code –
  nächstes Mal Schätzungen konsequent kurz halten.
- Am Anfang fehlte eine klare Definition of Done; dadurch war unklar, wann
  ein Issue wirklich fertig ist.
- Der Code-Review fiel mir schwer, weil „fremder Code“ in der
  Einzelarbeit oft der eigene ist – Perspektivwechsel ist anstrengend.

## Maßnahmen für den nächsten Sprint (mindestens 3)

1. **DoD vor dem Sprint festlegen:** Jedes Issue bekommt vor der Arbeit
   explizite Akzeptanzkriterien, die auch wirklich abgehakt werden.
2. **Zeitbox für Schätzungen:** Aufwandsschätzung auf 10 Minuten begrenzen,
   dann entscheiden – Perfektionismus vermeiden.
3. **Review-Sprache üben:** Mindestens einmal pro Woche fremden Code (z. B.
   aus Open-Source-Projekten) mit Datei/Zeile/Vorschlag kommentieren.
4. **CI-Gewohnheit:** Nach jedem Commit `python3 notenspiegel.py` (und die
   Tests) ausführen – so bleibt der Branch immer grün.
"""

# ---------------------------------------------------------------------------
# Hauptprogramm – die 7 Schritte der Aufgabe
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    ziel = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd() / "notenspiegel"
    projekt = ziel.resolve()

    if projekt.exists() and any(projekt.iterdir()):
        sys.exit(f"FEHLER: {projekt} existiert bereits und ist nicht leer. "
                 "Bitte leeren Zielordner wählen.")

    print(f"=== Schritt 1: Projekt anlegen ({projekt}) ===")
    projekt.mkdir(parents=True)
    schreibe_datei(projekt / "README.md", README)
    schreibe_datei(projekt / ".gitignore", "notenspiegel.pyc\n__pycache__/\n")
    git(projekt, "init", "-b", "main")
    git_config_sicherstellen(projekt)
    git(projekt, "add", "README.md", ".gitignore")
    git(projekt, "commit", "-m", "Add README und .gitignore")

    print("=== Schritt 2: Backlog & Issues ===")
    schreibe_datei(projekt / "docs" / "issues.md", ISSUES)
    git(projekt, "add", "docs/issues.md")
    git(projekt, "commit", "-m", "Add Issue-Backlog (docs/issues.md)")

    print("=== Schritt 3: Sprint-Planung ===")
    schreibe_datei(projekt / "docs" / "sprint_planung.md", SPRINT_PLANUNG)
    git(projekt, "add", "docs/sprint_planung.md")
    git(projekt, "commit", "-m", "Add Sprint-Planung (docs/sprint_planung.md)")

    print("=== Schritt 4: Feature-Branch & Arbeit ===")
    git(projekt, "checkout", "-b", "feature/notenspiegel")
    schreibe_datei(projekt / "notenspiegel.py", NOTENSPIEGEL_V1)
    git(projekt, "add", "notenspiegel.py")
    git(projekt, "commit", "-m", "Add Notenspiegel-Ausgabe (Issue #1)")
    # Zweiter, sinnvoller Commit: Durchschnitt + beste Note (Issues #3, #4)
    schreibe_datei(projekt / "notenspiegel.py", NOTENSPIEGEL_V2)
    git(projekt, "add", "notenspiegel.py")
    git(projekt, "commit", "-m", "Add Durchschnitt und beste Note (Issues #3, #4)")

    print("=== Schritt 5: Pull Request ===")
    # Terminal-Ausgabe des Tools als „Screenshot“ für den PR erfassen
    ausgabe = subprocess.run(
        ["python3", "notenspiegel.py"],
        cwd=projekt,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    schreibe_datei(projekt / "docs" / "pull_request.md", pull_request_dokument(ausgabe))
    schreibe_datei(projekt / "docs" / "review.md", REVIEW)
    schreibe_datei(projekt / "docs" / "retrospektive.md", RETROSPEKTIVE)
    git(projekt, "add", "docs/pull_request.md", "docs/review.md", "docs/retrospektive.md")
    git(projekt, "commit", "-m", "Add PR-Unterlagen, Code-Review und Retrospektive")

    print("=== Schritt 6 & 7 erledigt: Review und Retrospektive sind in docs/ ===")
    print("\n=== Ergebnis: Git-Historie ===")
    print(git(projekt, "log", "--oneline", "--all").stdout)
    print("=== Branches ===")
    print(git(projekt, "branch").stdout)
    print(f"Fertig! Projekt liegt unter: {projekt}")
