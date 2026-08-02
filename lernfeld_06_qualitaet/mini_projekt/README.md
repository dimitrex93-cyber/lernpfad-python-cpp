# Mini-Projekt Lernfeld 6: Abschlussprojekt mit Tests, CI und Doku

Das Abschlussprojekt des Moduls **Qualität & Projektmanagement** – und der
krönende Abschluss des gesamten Lernpfads. Es kombiniert alles, was du in
Lernfeld 6 gelernt hast: Unit-Tests, Test-first (TDD), Debugging, Refactoring,
Clean Code, Git-Workflow und Projektmanagement.

> 🚫 **Bewusst ohne Musterlösung.** Das Projekt ist dein eigenes – du bist jetzt
> dran. Wenn du eine Lösung als Pull Request beisteuern willst, lies zuerst
> [CONTRIBUTING.md](../../CONTRIBUTING.md).

## Aufgabe

Baue dein **eigenes Abschlussprojekt** – ein Programm deiner Wahl, das du
professionell entwickelst. Wichtig ist nicht (nur) der Code, sondern der
**Prozess**: Du gehst den kompletten Weg wie ein Software-Entwickler im Team.

**Ideen (oder eigene wählen):**
- erweiterte Notizverwaltung mit Tags & Statistik
- To-Do-Liste mit Prioritäten und Fälligkeitsdaten
- Spesen-/Zeiterfassung mit Monatsübersicht
- kleiner Währungsrechner mit Historie

**Pflicht-Anforderungen:**
1. **Test-first:** Schreibe zuerst die Tests, dann den Code (TDD).
2. **Mindestens 10 Unit-Tests** für die Kernlogik (Python: `unittest`/`pytest`,
   C++: doctest/Catch2 – wie in Aufgabe 1 gelernt).
3. **Sauberer Code:** Funktionen < 20 Zeilen, sprechende Namen, keine
   Duplikate (Refactoring wie in Aufgabe 4).
4. **README.md** für dein Projekt: Beschreibung, Installation, Nutzung.
5. **Git-Workflow:** eigene Branches für Features, aussagekräftige Commits,
   am Ende einen Merge.
6. **Doku:** Kommentare nur wo nötig, aber dafür gut.

## Beispiel-Ablauf (TDD)

```
$ python3 -m unittest test_notizen.py
..F...                                 (1 Test schlägt fehl – Rot)
→ Implementierung schreiben
$ python3 -m unittest test_notizen.py
...........                            (alle grün – Grün)
→ Aufräumen (Refactoring)              (Refactor)
```

## Umsetzung: erst Python, dann C++

Wie im ganzen Kurs: Baue zuerst die **Python-Version** (schnell, `unittest`),
danach die **C++-Version** (mit doctest – als einzelne Header-Datei, kein
externes Installieren nötig).

### Python
- Dateien: `projekt.py`, `test_projekt.py` (in deinem eigenen Ordner!)
- Tests: `python3 -m unittest test_projekt.py -v`
- Ausführen: `python3 projekt.py`

### C++
- Dateien: `projekt.cpp`, `test_projekt.cpp`
- Kompilieren (doctest ist ein einzelner Header, z. B. `doctest.h`):
  `g++ -std=c++17 -Wall -Wextra test_projekt.cpp -o tests`
- **Null Warnungen sind Pflicht** – das ist Teil der Aufgabe!
- Ausführen: `./tests`

## Abnahme-Kriterien (Selbsttest)

- [ ] Ich habe zuerst Tests geschrieben, dann Code (TDD eingehalten)
- [ ] Mindestens 10 Unit-Tests, alle grün
- [ ] Funktionen sind klein, Namen sprechend, kein Copy-Paste
- [ ] README.md erklärt Installation und Nutzung
- [ ] Ich habe mit Branches und sinnvollen Commits gearbeitet
- [ ] C++-Version kompiliert mit `-Wall -Wextra` ohne Warnungen
- [ ] Ich kann jede Zeile meines Codes erklären 💪

## Erweiterungen (Bonus – wähle mindestens eine)

- [ ] **CI:** GitHub Actions-Workflow, der bei jedem Push die Tests ausführt
- [ ] **Code-Coverage** messen (Python: `coverage.py`)
- [ ] **CLI-Argumente** (`argparse` / `getopt`) statt starrer Menüführung
- [ ] **Projekt-Plan** als Issue-Tracker im GitHub-Repo führen (Milestones,
  Issues, Labels – wie in Aufgabe 5 geplant)

## Fertig? Dann…

- [ ] Haken in der [checklist.md](../checklist.md) setzen
- [ ] [vergleich.md](../vergleich.md) lesen, falls noch nicht geschehen
- [ ] 🏆 **Herzlichen Glückwunsch – du hast den Lernpfad abgeschlossen!**
      Du bist vom Anfänger zum Senior-Entwickler durchgelaufen. Zeig dein
      Abschlussprojekt auf GitHub, dein Portfolio ist komplett! 🎉
