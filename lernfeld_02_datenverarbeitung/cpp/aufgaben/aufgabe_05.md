# Aufgabe 5: Laufzeit-Vergleich – Python vs. C++ (C++)

**Schwierigkeit:** ⭐⭐⭐⭐ · **Themen:** `<chrono>`, `<random>`, `std::vector`, Performance-Messung

> 📄 Die Aufgabenstellung ist dieselbe wie in Python – lies dort zuerst
> **Lernziele** und **Beispiel**: [`../python/aufgaben/aufgabe_05.md`](../python/aufgaben/aufgabe_05.md)

## Aufgabenstellung (Kurzfassung)

100.000 Zufallszahlen erzeugen und sortieren, dann **100.000 binäre Suchen**
(aus Aufgabe 3) durchführen – und nur die **Suchzeit** mit `<chrono>` messen.
Ergebnis mit der Python-Version vergleichen.

## C++-spezifische Hinweise

- **Includes:** `<chrono>`, `<random>`, `<vector>`, `<algorithm>`, `<iostream>`,
  `<iomanip>`.
- **Zeitmessung mit `<chrono>`** – das Pendant zu `time.perf_counter()`:

  ```cpp
  #include <chrono>
  auto start = std::chrono::high_resolution_clock::now();
  // ... Suchschleife ...
  auto ende = std::chrono::high_resolution_clock::now();
  double dauer = std::chrono::duration<double>(ende - start).count();
  std::cout << "Suchzeit: " << std::fixed << std::setprecision(3)
            << dauer << " Sekunden" << std::endl;
  ```

  `duration<double>` rechnet die Differenz automatisch in Sekunden um.
  `std::fixed`/`std::setprecision` kommen aus `<iomanip>`.
- **Zufallszahlen modern** – `rand()` ist veraltet; nimm die C++11-
  Zufallsbibliothek:

  ```cpp
  #include <random>
  std::mt19937 generator(42);   // fester Startwert = reproduzierbar
  std::uniform_int_distribution<int> verteilung(0, 1'000'000);

  std::vector<int> zahlen(100'000);
  for (int& x : zahlen) x = verteilung(generator);
  ```

  Der feste Startwert `42` ist der Trick für den **fairen Vergleich**: Python
  nutzt `random.seed(42)` – so bekommen beide Sprachen dieselben Daten!
  (`1'000'000` mit Apostroph ist C++14+-Schreibweise für 1 Million.)
- **Sortieren:** `std::sort(zahlen.begin(), zahlen.end());` – ja, hier ist
  `std::sort` erlaubt (es geht um die Suche). `std::sort` ist in C++
  implementiert und Teil der Sprache – in Python steckt hinter `sorted()`
  ebenfalls C-Code. Deshalb ist das Sortieren in beiden Sprachen ähnlich
  schnell – die große Lücke entsteht in den **Schleifen**, die du selbst
  schreibst (die binäre Suche!).
- **Suchschleife:** 100.000 Suchwerte erzeugen, dann für jeden
  `binaere_suche(zahlen, wert)` aufrufen. Miss **nur** die Suchschleife, nicht
  das Erzeugen der Daten!
- **Optimierung beim Kompilieren** – jetzt wird C++ ernst:

  ```bash
  g++ -std=c++17 -O2 -Wall -Wextra loesung_05.cpp -o loesung_05
  ```

  `-O2` schaltet die Optimierungen an. Erst jetzt zeigt C++, was es kann –
  und der Vergleich mit Python wird fair (Pythons `sorted()` ist ja auch
  optimierter C-Code).
- **Erwartung:** Deine C++-Suchzeit wird typischerweise **50–100× kleiner**
  sein als die Python-Zeit. Falls nicht: Messung prüfen (Optimierung vergessen?
  Suchwerte mitgemessen? Liste nicht sortiert?).

## Erweiterung (Bonus)

- **Lineare Suche** ebenfalls messen und die O(n)- gegen O(log n)-Zeit zeigen.
- **Bubble Sort** (Aufgabe 2) auf 10.000 Zahlen messen – Achtung: O(n²) lässt
  grüßen, bei 100.000 Elementen würdest du Minuten warten.
- Durchschnittliche Zeit pro Suche in Mikrosekunden ausgeben
  (`dauer / 100'000 * 1'000'000`).

## Selbsttest

- [ ] 100.000 Zufallszahlen werden erzeugt und sortiert
- [ ] 100.000 binäre Suchen laufen durch
- [ ] Die Messung umfasst nur die Suchschleife
- [ ] Ausgabe in Sekunden mit 3 Nachkommastellen
- [ ] Gleicher Startwert wie in Python (`seed(42)`) → vergleichbare Daten
- [ ] Kompiliert mit `-std=c++17 -O2 -Wall -Wextra` (null Warnungen)
- [ ] C++-Zeit ist dokumentiert und mit der Python-Zeit verglichen

---

**Fertig mit den Aufgaben!** Weiter geht's im [Lernfeld-README](../../README.md) –
Theorie, Checkliste und Mini-Projekt folgen dort.
