# Lernfeld 1 – Aufgaben (C++)

Hier findest du die **C++-Versionen** der Übungsaufgaben aus dem Modul Grundlagen.
Du hast jede Aufgabe bereits in Python gelöst – jetzt setzt du **dieselbe Idee**
in C++ um. Genau dieser Wechsel ist der didaktische Kern des Kurses.

| Aufgabe | Thema | Schwierigkeit |
|---|---|---|
| [Aufgabe 1](aufgabe_01.md) | Persönliche Begrüßung (Ein-/Ausgabe, Variablen) | ⭐ |
| [Aufgabe 2](aufgabe_02.md) | Temperaturumrechner (Schleifen, Menü, Funktionen) | ⭐⭐ |
| [Aufgabe 3](aufgabe_03.md) | Zahlenraten (Zufall, Bedingungen, Schleifen) | ⭐⭐ |
| [Aufgabe 4](aufgabe_04.md) | Notenverwaltung (`std::vector`, Funktionen) | ⭐⭐⭐ |
| [Aufgabe 5](aufgabe_05.md) | Textanalyse (Strings, `std::map`) | ⭐⭐⭐ |

## So arbeitest du

1. Aufgabenstellung lesen – sie ist dieselbe wie in Python. Der Unterschied liegt
   in den **C++-spezifischen Hinweisen** pro Aufgabe.
2. Eigene Lösung schreiben, z. B. `loesung_01.cpp`.
3. Kompilieren mit **allen Warnungen an**:

   ```bash
   g++ -std=c++17 -Wall -Wextra loesung_01.cpp -o loesung_01
   ```

4. Ausführen: `./loesung_01`
5. **Null Warnungen** = fertig kompiliert. Erst danach die Musterlösung in
   `../loesungen/` ansehen.
6. Haken in `../checklist.md` setzen.

> 💡 **Merke:** Compiler-Fehlermeldungen sind keine Niederlage, sondern der
> Compiler als strenger Lehrer. Lies die erste Meldung, finde Zeile und Spalte,
> behebe, kompiliere erneut. Die C++-Theorie hat eine Fehler-Tabelle in Kapitel 12.

## C++-Checkliste für jede Aufgabe

- [ ] `#include` für alles, was du nutzt (`<iostream>`, `<string>`, `<vector>` …)
- [ ] `int main()` als Einstiegspunkt, `return 0;` am Ende
- [ ] Semikolon `;` nach jeder Anweisung
- [ ] Typen angesagt: `int`, `double`, `std::string` …
- [ ] Ganzzahl-Division bedacht (Tipp: `double` verwenden!)
- [ ] Kompiliert mit `-std=c++17 -Wall -Wextra` ohne Warnungen
