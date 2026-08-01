# Aufgabe 5: Projektmanagement & Git-Workflow

**Schwierigkeit:** ⭐⭐⭐⭐⭐ · **Themen:** Git, Branches, Issues, Pull Requests, Code-Review, Scrum-Rollen, Retrospektive, README

## Lernziele

- [ ] ein Git-Repository für ein Mini-Projekt anlegen und strukturiert committen
- [ ] Issues mit Priorität und Akzeptanzkriterien formulieren
- [ ] einen Feature-Branch anlegen und einen Pull Request beschreiben (Vorlage)
- [ ] fremden Code konstruktiv reviewen (Kommentare mit Datei, Zeile, Vorschlag)
- [ ] eine Sprint-Planung mit Scrum-Rollen (PO, SM, Dev) durchführen
- [ ] eine Retrospektive schreiben und konkrete Maßnahmen ableiten

## Aufgabenstellung

Dies ist eine **Prozess-Aufgabe**: Du planst und simulierst ein kleines
Projekt so, wie es im Berufsalltag abläuft – mit Git, Issues, Pull Request,
Code-Review und Scrum. Dein Projekt: das **Notenspiegel-Tool** aus Aufgabe 4
(du darfst deinen refaktorierten Code dafür wiederverwenden).

Du spielst dabei **alle Scrum-Rollen selbst** – als Einzelperson übernimmst du
nacheinander die Perspektiven von Product Owner, Scrum Master und
Development-Team. Das ist ein Rollenspiel: Notiere zu jeder Rolle, was du in
ihr entscheidest.

Arbeite die Schritte **in dieser Reihenfolge** ab:

1. **Projekt anlegen:** Erstelle einen neuen Ordner `notenspiegel/`, dort
   `git init`. Schreibe eine `README.md` mit: Projektname, Ziel (1–2 Sätze),
   Funktionen (Liste), Bedienung (Terminal-Befehle), verwendete Sprache.
2. **Backlog & Issues:** Lege `docs/issues.md` an und formuliere **mindestens
   3 Issues** (z. B. „Notenspiegel ausgeben“, „Noten-Eingabe validieren“,
   „Durchschnitt berechnen“). Jedes Issue mit Typ, Priorität, Beschreibung
   und Akzeptanzkriterien (Checkliste).
3. **Sprint-Planung:** Wähle als **Product Owner** die Issues für den ersten
   Sprint aus und priorisiere sie. Formuliere ein **Sprint-Ziel** (ein Satz).
   Als **Scrum Master** überlegst du, welche Hindernisse (Risiken) auftauchen
   könnten. Als **Dev-Team** schätzt du den Aufwand (klein/mittel/groß).
4. **Feature-Branch & Arbeit:** Lege einen Branch an:
   `git checkout -b feature/notenspiegel`. Setze die Issues aus Schritt 3 in
   **mehreren sinnvollen Commits** um – nicht alles in einem Rutsch!
   Zwischendurch: `git status`, `git log --oneline` prüfen.
5. **Pull Request:** Simuliere die Zusammenführung: Beschreibe deinen PR in
   `docs/pull_request.md` mit der **Vorlage unten**. Füge als „Screenshot“
   die Terminal-Ausgabe deines Tools als Codeblock ein.
6. **Code-Review:** Review den fremden Code unten (ein Auszug aus einem
   imaginären PR eines Kollegen). Schreibe **mindestens 3 Review-Kommentare**
   in `docs/review.md` – mit Datei, Zeile, Problem und konkretem Vorschlag.
7. **Retrospektive:** Schreibe `docs/retrospektive.md` nach dem Sprint:
   Was lief gut? Was lief schlecht? Welche **Maßnahmen** nimmst du für den
   nächsten Sprint mit? (Mindestens 3 Maßnahmen.)

### PR-Vorlage (für `docs/pull_request.md`)

```markdown
# Pull Request: <Kurztitel>

**Branch:** feature/notenspiegel → main
**Behebt Issues:** #<Nr>, #<Nr>

## Beschreibung
<Was macht dieser PR? Warum? (2–3 Sätze)>

## Änderungen
- <Datei>: <was wurde geändert>
- <Datei>: <was wurde geändert>

## Getestet
- [ ] `python3 notenspiegel.py` liefert korrekte Ausgabe
- [ ] Randfall: leere Eingabe stürzt nicht ab
- [ ] <weiterer Test>

## Ausgabe
```text
<deine Terminal-Ausgabe hier>
```

## Checkliste
- [ ] Code kommentiert, wo nötig
- [ ] Keine Debug-Ausgaben
- [ ] README aktualisiert
```

### Fremder Code für das Code-Review (Schritt 6)

Ein Kollege hat in einem PR `noten_utils.py` eingereicht. Review ihn:

```python
def noten_durchschnitt(noten):
    summe = 0
    for note in noten:
        summe += note
    return summe / len(noten)


def beste(noten):
    beste = 6
    for note in noten:
        if note < beste:
            beste = note
    return beste


noten = [2, 4, 1, 3]
print("Durchschnitt:", noten_durchschnitt(noten))
print("Beste Note:", beste(noten))
```

## Beispiel (Ein-/Ausgabe)

Ein **Review-Kommentar** hat immer dieselbe Form – konkret, sachlich und mit
Vorschlag (nicht: „das ist schlecht“, sondern: „hier fehlt X, so geht's“):

| Datei | Zeile | Problem | Vorschlag |
|---|---|---|---|
| `noten_utils.py` | 5 | `len(noten)` ist 0 bei leerer Liste → `ZeroDivisionError` | Leere Liste vorher prüfen und `ValueError` mit Meldung werfen |
| `noten_utils.py` | 8–13 | Name `beste` ist mehrdeutig („beste“ = kleinste Note?) und `6` ist eine magische Zahl | Umbenennen in `beste_note`, Startwert als Konstante `MAX_NOTE = 6` oder aus `noten[0]` ableiten |
| `noten_utils.py` | 1 | Kein Docstring, keine Typhinweise | `def notendurchschnitt(noten: list[float]) -> float:` + ein Satz im Docstring |

*(Schreibe selbst mindestens 3 solcher Kommentare – auch zu Stellen, die hier
nicht genannt sind.)*

## Hinweise

- **Git-Befehle für den Workflow:**

  ```bash
  git init                       # Repository anlegen
  git status                     # Änderungen anzeigen
  git add README.md              # Datei vormerken
  git commit -m "README hinzugefügt"
  git checkout -b feature/notenspiegel   # neuer Branch + Wechsel
  git log --oneline              # Commit-Historie kompakt
  git diff                       # ungespeicherte Änderungen zeigen
  ```

- **Commit-Meldungen** im Imperativ schreiben („Add“, „Fix“, „Rename“):
  `git commit -m "Add Notenspiegel-Ausgabe"` – das ist ein weltweiter
  Standard (auch in deutschen Teams schreibt man Commits meist auf Englisch).
- **Scrum-Rollen** – kurz zusammengefasst:
  - **Product Owner (PO):** entscheidet, *was* gebaut wird (Backlog,
    Prioritäten, Anforderungen).
  - **Scrum Master (SM):** sorgt dafür, dass der Prozess läuft, räumt
    Hindernisse aus dem Weg.
  - **Dev-Team:** baut das Produkt und schätzt den Aufwand.
- **Definition of Done (DoD):** Lege fest, wann ein Issue *wirklich fertig*
  ist (z. B. „Code läuft, Randfälle getestet, README aktuell, Commit gepusht“).
- **Review-Regeln:** Kommentare beziehen sich auf **Datei und Zeile**, nennen
  das **Problem** und einen **konkreten Vorschlag**. Ton: sachlich und
  respektvoll – du reviewst den Code, nicht die Person.
- **Retrospektive** ist kein Schuldzuweisungs-Ritual: ehrlich benennen, was
  gut lief, und **umsetzbare** Verbesserungen wählen (nicht 20, sondern 3!).

## Erweiterung (Bonus)

- Lege das Repository auf **GitHub/GitLab** an (Remote hinzufügen,
  `git push`), erstelle dort echte Issues und einen echten Pull Request.
- Richte eine **CI-Pipeline** ein (z. B. GitHub Actions), die bei jedem Push
  `python3 -m pytest` ausführt – so bekommst du den „grünen Haken“.
- Schätze die Issues mit **Story Points** (1, 2, 3, 5, 8) statt klein/mittel/groß
  und zeichne ein einfaches Burndown-Diagramm (Terminal-ASCII reicht).

## Selbsttest

- [ ] `git init` durchgeführt, Ordner `notenspiegel/` mit `README.md`
- [ ] `docs/issues.md` mit mindestens 3 Issues inkl. Priorität und
      Akzeptanzkriterien
- [ ] Sprint-Planung dokumentiert: Sprint-Ziel, priorisiertes Backlog,
      Rollen-Blickwinkel (PO/SM/Dev) erkennbar
- [ ] Branch `feature/notenspiegel` existiert (`git branch`), mehrere
      sinnvolle Commits (`git log --oneline`)
- [ ] `docs/pull_request.md` mit ausgefüllter Vorlage inkl. Terminal-Ausgabe
- [ ] `docs/review.md` mit mindestens 3 konkreten Review-Kommentaren
- [ ] `docs/retrospektive.md` mit Was-gut/was-schlecht und mindestens
      3 Maßnahmen

---

**Danach:** Löse dieselbe Aufgabe in C++: `../../cpp/aufgaben/aufgabe_05.md`
