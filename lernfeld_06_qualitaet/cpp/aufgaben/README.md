# Lernfeld 6 – Aufgaben (C++)

Hier findest du die **C++-Versionen** der Übungsaufgaben aus dem Modul
Softwarequalität. Du hast jede Aufgabe bereits in Python gelöst – jetzt setzt
du **dieselbe Idee** in C++ um. Genau dieser Wechsel ist der didaktische Kern
des Kurses.

| Aufgabe | Thema | Schwierigkeit |
|---|---|---|
| [Aufgabe 1](aufgabe_01.md) | Unit-Tests für den Temperaturumrechner (`assert`, doctest) | ⭐⭐ |
| [Aufgabe 2](aufgabe_02.md) | Test-first: Notendurchschnitt mit TDD (Red-Green-Refactor) | ⭐⭐⭐ |
| [Aufgabe 3](aufgabe_03.md) | Debugging: drei versteckte Bugs finden und fixen | ⭐⭐⭐ |
| [Aufgabe 4](aufgabe_04.md) | Refactoring: Notenspiegel-Code wird Clean Code | ⭐⭐⭐⭐ |
| [Aufgabe 5](aufgabe_05.md) | Projektmanagement & Git-Workflow (Issues, PR, Scrum) | ⭐⭐⭐⭐⭐ |

## So arbeitest du

1. Aufgabenstellung lesen – sie ist dieselbe wie in Python. Der Unterschied
   liegt in den **C++-spezifischen Hinweisen** pro Aufgabe.
2. Eigene Lösung schreiben, z. B. `test_temperatur.cpp`, `notenspiegel.cpp`.
3. Kompilieren mit **allen Warnungen an**:

   ```bash
   g++ -std=c++17 -Wall -Wextra deine_datei.cpp -o deine_datei
   ```

4. Ausführen: `./deine_datei`
5. **Null Warnungen** = sauber kompiliert. Erst dann weitergehen.

> 💡 **Merke:** Compiler-Fehlermeldungen sind keine Niederlage, sondern der
> Compiler als strenger Lehrer. Lies die erste Meldung, finde Zeile und
> Spalte, behebe, kompiliere erneut.
>
> 💡 **Hinweis zu Musterlösungen:** In Lernfeld 6 gibt es bewusst **keine
> Musterlösungen** – Qualität beurteilst du selbst: mit den Testfällen aus
> den Aufgaben, dem **Selbsttest** und der Klausur in `../test/test.md`.
> Bitte bei Unsicherheit eine andere Person um ein **Code-Review**!
>
> 💡 **Test-Framework:** Für einfache Fälle reicht `assert()` aus `<cassert>`.
> Für echte Test-Suiten: **doctest** (Single-Header `doctest.h`) oder
> **Catch2** – siehe [Aufgabe 1](aufgabe_01.md).

## C++-Checkliste für jede Aufgabe

- [ ] `#include` für alles, was du nutzt (`<iostream>`, `<vector>`, `<map>`, `<cassert>` …)
- [ ] `int main()` als Einstiegspunkt, `return 0;` am Ende
- [ ] Semikolon `;` nach jeder Anweisung
- [ ] Typen angesagt und an die Problemdomäne angepasst (`double`, nicht `int` bei Noten!)
- [ ] Container per `const&` übergeben, wenn sie nur gelesen werden
- [ ] Ganzzahl-Division bedacht (Stichwort `int / int`)
- [ ] Kompiliert mit `-std=c++17 -Wall -Wextra` ohne Warnungen
