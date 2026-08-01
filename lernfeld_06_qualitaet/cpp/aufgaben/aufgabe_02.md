# Aufgabe 2: Test-first – Notendurchschnitt mit TDD (C++)

**Schwierigkeit:** ⭐⭐⭐ · **Themen:** TDD (Red-Green-Refactor), `assert()`, `std::vector`, `std::invalid_argument`, Linker-Fehler als „Rot“

> 📄 Die Aufgabenstellung ist dieselbe wie in Python – lies dort zuerst
> **Lernziele** und **Beispiel**: [`../python/aufgaben/aufgabe_02.md`](../python/aufgaben/aufgabe_02.md)

## Aufgabenstellung (Kurzfassung)

Baue `double notendurchschnitt(const std::vector<double>& noten)` mit
**Test-first**: erst Tests, dann Implementierung (RED → GREEN → REFACTOR).
Gültige Noten: `1.0`–`6.0`. Leere Liste und ungültige Werte werfen
`std::invalid_argument` mit verständlicher Meldung.

## C++-spezifische Hinweise

- **C++ hat kein pytest** – die Tests sind `assert()`-Zeilen in `main()`
  (oder doctest/Catch2, siehe Aufgabe 1). Der „Test-Runner“ ist dein
  Programm selbst: Es beendet sich still mit Exit-Code 0, wenn alles grün ist.

  ```cpp
  // test_notendurchschnitt.cpp
  #include <cassert>
  #include <vector>
  #include "notendurchschnitt.h"

  int main() {
      assert(notendurchschnitt({2.0, 3.0, 1.0}) == 2.0);
      assert(notendurchschnitt({4.0}) == 4.0);
      assert(notendurchschnitt({1.0, 6.0}) == 3.5);

      // Exceptions testen: try/catch erwartet, dass eine Exception kommt
      bool leer_geworfen = false;
      try { notendurchschnitt({}); }
      catch (const std::invalid_argument&) { leer_geworfen = true; }
      assert(leer_geworfen);

      return 0;
  }
  ```

- **RED in C++ funktioniert anders als in Python:** Ohne
  `notendurchschnitt.h`/`.cpp` bekommst du einen **Linker-Fehler**
  (`undefined reference`), nicht zur Laufzeit. Deshalb ist der saubere
  TDD-Weg in C++:

  1. Header `notendurchschnitt.h` mit der **Signatur** schreiben.
  2. In `notendurchschnitt.cpp` einen **Stub** hinterlegen, der bewusst
     falsch ist (z. B. `return 0.0;`). Jetzt kompiliert alles, aber die
     Tests schlagen zur Laufzeit fehl – das ist dein **rotes** Bild.
  3. Erst jetzt die echte Berechnung + Validierung implementieren
     (→ **grün**).
  4. Refactoring – Tests bleiben grün.
- **Exception werfen** (Pendant zu Pythons `raise ValueError`):

  ```cpp
  #include <stdexcept>
  if (noten.empty()) {
      throw std::invalid_argument("Notenliste darf nicht leer sein");
  }
  ```

- **Gleitkommazahlen:** `3.5` ist exakt darstellbar, aber vergleiche
  Ergebnisse wie `(1.0 + 2.0) / 3.0` nie exakt mit `==`. Toleranz-Vergleich:

  ```cpp
  double d = notendurchschnitt({1.0, 2.0, 3.0});
  assert(d > 1.999 && d < 2.001);
  ```

- **Kompilieren:**

  ```bash
  g++ -std=c++17 -Wall -Wextra notendurchschnitt.cpp test_notendurchschnitt.cpp -o test_noten
  ./test_noten && echo "ALLE TESTS GRUEN"
  ```

  `&&` führt den `echo` nur aus, wenn das Programm mit Exit-Code 0 endet.
- **Braced init list:** `notendurchschnitt({2.0, 3.0, 1.0})` funktioniert,
  weil der Parameter `const std::vector<double>&` ist.

## Erweiterung (Bonus)

- **FizzBuzz in Runde 2:** `std::string fizzbuzz(int n)` test-first –
  `"Fizz"` bei Teilbarkeit durch 3, `"Buzz"` durch 5, `"FizzBuzz"` durch
  beides, sonst `std::to_string(n)`.
- Stelle auf **doctest** um (siehe Aufgabe 1): Mit `CHECK_THROWS_AS(...,
  std::invalid_argument)` testest du Exceptions viel eleganter.
- Runde das Ergebnis auf 2 Nachkommastellen (mit `std::round` aus `<cmath>`
  und einem Testfall dazu).

## Selbsttest

- [ ] Tests wurden **vor** der Implementierung geschrieben (Stub = rot)
- [ ] `notendurchschnitt.cpp` wirft bei leerer Liste und Noten < 1.0 / > 6.0
      `std::invalid_argument`
- [ ] `./test_noten && echo "ALLE TESTS GRUEN"` gibt die Meldung aus
- [ ] Kompiliert fehlerfrei mit `-std=c++17 -Wall -Wextra` (null Warnungen)
- [ ] Nach dem Refactoring laufen die Tests weiterhin grün durch

---

**Weiter:** [`aufgabe_03.md`](aufgabe_03.md)
