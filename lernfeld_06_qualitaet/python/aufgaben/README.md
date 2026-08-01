# Lernfeld 6 – Aufgaben (Python)

Hier findest du die praktischen Übungsaufgaben zum Modul **Softwarequalität,
Testing und Projektmanagement**. Bearbeite sie **in Reihenfolge** – der
Schwierigkeitsgrad steigt.

| Aufgabe | Thema | Schwierigkeit |
|---|---|---|
| [Aufgabe 1](aufgabe_01.md) | Unit-Tests für den Temperaturumrechner (pytest) | ⭐⭐ |
| [Aufgabe 2](aufgabe_02.md) | Test-first: Notendurchschnitt mit TDD (Red-Green-Refactor) | ⭐⭐⭐ |
| [Aufgabe 3](aufgabe_03.md) | Debugging: drei versteckte Bugs finden und fixen | ⭐⭐⭐ |
| [Aufgabe 4](aufgabe_04.md) | Refactoring: Notenspiegel-Code wird Clean Code | ⭐⭐⭐⭐ |
| [Aufgabe 5](aufgabe_05.md) | Projektmanagement & Git-Workflow (Issues, PR, Scrum) | ⭐⭐⭐⭐⭐ |

## So arbeitest du

1. Aufgabenstellung genau lesen und das **Beispiel** (Ein-/Ausgabe) verstehen.
2. Eigene Dateien schreiben – z. B. `temperatur.py`, `test_temperatur.py`,
   `noten_statistik.py` **in deinem eigenen Ordner**.
3. Programm ausführen: `python3 deine_datei.py`
4. Tests ausführen: `python3 -m pytest`
5. **Selbsttest** in der Aufgabe abhaken – und erst dann weitergehen.

> 💡 **Hinweis zu Musterlösungen:** In Lernfeld 6 gibt es bewusst **keine
> Musterlösungen** – Qualität beurteilst du selbst: mit den Testfällen aus den
> Aufgaben, dem **Selbsttest** und der Klausur in `../test/test.md`. Wenn du
> unsicher bist, ob deine Lösung gut ist: Bitte eine andere Person um ein
> **Code-Review** – genau darum geht es in diesem Modul!
>
> 💡 **Tipp:** Die Aufgaben 1–4 bauen aufeinander auf (Temperaturumrechner →
> TDD → Debugging → Refactoring). Deine Lösung aus Aufgabe 4 brauchst du in
> Aufgabe 5 wieder – heb sie gut auf!

## Allgemeine Hinweise

- Nur die **Python-Standardbibliothek** – für pytest gilt:
  `pip install pytest` (einmalig) oder `python3 -m pytest` nach Installation.
- Schreibe lesbaren Code: aussagekräftige Namen, kleine Funktionen, Kommentare.
- Jede Aufgabe hat eine **Erweiterung (Bonus)** – mach sie, wenn die Basis steht.
- Die Themen des Moduls (Theorie-Kapitel) stehen in `../theorie/README.md`.
