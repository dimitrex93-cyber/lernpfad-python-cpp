# Lernfeld 2 – Aufgaben (C++)

Hier findest du die **C++-Versionen** der Übungsaufgaben aus dem Modul
**Einfache Datenverarbeitung und Algorithmen**. Du hast jede Aufgabe bereits in
Python gelöst – jetzt setzt du **dieselbe Idee** in C++ um. Genau dieser
Wechsel ist der didaktische Kern des Kurses.

| Aufgabe | Thema | Schwierigkeit |
|---|---|---|
| [Aufgabe 1](aufgabe_01.md) | Zahlenstatistik aus Datei (`std::ifstream`, `std::vector`) | ⭐⭐ |
| [Aufgabe 2](aufgabe_02.md) | Bubble Sort selbst gebaut (`std::vector`, `std::swap`) | ⭐⭐ |
| [Aufgabe 3](aufgabe_03.md) | Binäre Suche (Suchalgorithmen, Indexberechnung) | ⭐⭐⭐ |
| [Aufgabe 4](aufgabe_04.md) | Wortfrequenz-Analyse (`std::map`, Ranking) | ⭐⭐⭐ |
| [Aufgabe 5](aufgabe_05.md) | Laufzeit-Vergleich Python vs. C++ (`<chrono>`, `<random>`) | ⭐⭐⭐⭐ |

## So arbeitest du

1. Aufgabenstellung lesen – sie ist dieselbe wie in Python. Der Unterschied
   liegt in den **C++-spezifischen Hinweisen** pro Aufgabe.
2. Eigene Lösung schreiben, z. B. `loesung_01.cpp`.
3. Kompilieren mit **allen Warnungen an**:

   ```bash
   g++ -std=c++17 -Wall -Wextra loesung_01.cpp -o loesung_01
   ```

   (Nur bei Aufgabe 5 zusätzlich `-O2`, damit die Zeitmessung fair ist.)
4. Ausführen: `./loesung_01`
5. **Null Warnungen** = sauber kompiliert. Testdaten wie `zahlen.txt` und
   `text.txt` selbst anlegen.
6. Haken im Selbsttest jeder Aufgabe setzen.

> 💡 **Merke:** In diesem Lernfeld treffen zwei C++-Klassiker aufeinander:
> die **Ganzzahl-Division** (`int / int` schneidet ab – mal gewollt wie bei der
> Indexberechnung, mal ein Fehler wie beim Durchschnitt) und **`std::size_t`**
> (`v.size()` ist unsigned – `v.size() - 1` kann riesig werden). Beide
> Stolpersteine sind in den Aufgaben markiert.

## C++-Checkliste für jede Aufgabe

- [ ] `#include` für alles, was du nutzt (`<fstream>`, `<vector>`, `<map>`, `<algorithm>` …)
- [ ] `int main()` als Einstiegspunkt, `return 0;` am Ende
- [ ] Datei-Öffnung geprüft (`is_open()`) – keine Abstürze bei fehlender Datei
- [ ] Ganzzahl-Division bedacht (Durchschnitt → `double`!)
- [ ] `v.size()`-/`-1`-Fallstricke bedacht (leere Vektoren)
- [ ] Funktionen mit `&`-Referenz, wenn sie den Vektor ändern sollen
- [ ] Kompiliert mit `-std=c++17 -Wall -Wextra` ohne Warnungen
