# Aufgabe 1: Unit-Tests für den Temperaturumrechner (C++)

**Schwierigkeit:** ⭐⭐ · **Themen:** Unit-Tests, `assert()` (`<cassert>`), doctest/Catch2, `g++ -std=c++17 -Wall -Wextra`, Gleitkommazahlen

> 📄 Die Aufgabenstellung ist dieselbe wie in Python – lies dort zuerst
> **Lernziele** und **Beispiel**: [`../python/aufgaben/aufgabe_01.md`](../python/aufgaben/aufgabe_01.md)

## Aufgabenstellung (Kurzfassung)

Nimm deinen Temperaturumrechner aus Lernfeld 1 (Aufgabe 2, C++-Version) bzw.
schreibe die Funktionen `celsius_nach_fahrenheit(double)` und
`fahrenheit_nach_celsius(double)` neu. Schreibe eine Testdatei mit
**mindestens 6 Testfällen** (Gefrierpunkt, Siedepunkt, `-40` als
Schnittpunkt der Skalen – in beide Richtungen). Alle Tests müssen grün sein.

## C++-spezifische Hinweise

- **Einfacher Weg – `assert()` aus `<cassert>`.** Für kleine Übungen reicht
  das völlig: Die Tests sind `assert(...)`-Zeilen in `main()`:

  ```cpp
  #include <cassert>
  #include "temperatur.h"

  int main() {
      assert(celsius_nach_fahrenheit(0.0) == 32.0);
      assert(celsius_nach_fahrenheit(100.0) == 212.0);
      assert(celsius_nach_fahrenheit(-40.0) == -40.0);
      assert(fahrenheit_nach_celsius(32.0) == 0.0);
      assert(fahrenheit_nach_celsius(212.0) == 100.0);
      assert(fahrenheit_nach_celsius(-40.0) == -40.0);
      // "Alle grün" heißt hier: main() läuft ohne Abbruch durch.
      return 0;
  }
  ```

  Schlägt ein `assert` fehl, bricht das Programm mit einer Meldung ab
  (`Assertion ... failed`) und einem Exit-Code ungleich 0.
- **Struktur mit Header** (so wie in Lernfeld 1 empfohlen):

  ```cpp
  // temperatur.h
  #ifndef TEMPERATUR_H
  #define TEMPERATUR_H
  double celsius_nach_fahrenheit(double c);
  double fahrenheit_nach_celsius(double f);
  #endif
  ```

  ```cpp
  // temperatur.cpp
  #include "temperatur.h"
  double celsius_nach_fahrenheit(double c) { return c * 9.0 / 5.0 + 32.0; }
  double fahrenheit_nach_celsius(double f) { return (f - 32.0) * 5.0 / 9.0; }
  ```

- **Kompilieren und ausführen:**

  ```bash
  g++ -std=c++17 -Wall -Wextra temperatur.cpp test_temperatur.cpp -o test_temperatur
  ./test_temperatur
  echo $?        # 0 = alle Tests bestanden, 1 (oder mehr) = assert fehlgeschlagen
  ```

  ⚠️ **Vergiss `temperatur.cpp` nicht beim Kompilieren** – sonst meldet der
  Linker „undefined reference“.
- **Gleitkommazahlen sind nie exakt!** `celsius_nach_fahrenheit(37.0)` ist
  nicht exakt `98.6`. Ein direkter `==`-Vergleich schlägt fehl. Vergleiche
  mit einer Toleranz:

  ```cpp
  double ergebnis = celsius_nach_fahrenheit(37.0);
  assert(ergebnis > 98.59 && ergebnis < 98.61);
  ```

  (doctest kann das automatisch: `CHECK(celsius_nach_fahrenheit(37.0) == doctest::Approx(98.6));`)
- **Framework-Weg (Bonus, wie pytest):** Lade `doctest.h` (Single-Header)
  von der doctest-Website und schreibe:

  ```cpp
  #define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
  #include "doctest.h"
  #include "temperatur.h"

  TEST_CASE("celsius nach fahrenheit") {
      CHECK(celsius_nach_fahrenheit(0.0) == 32.0);
      CHECK(celsius_nach_fahrenheit(100.0) == 212.0);
      CHECK(celsius_nach_fahrenheit(-40.0) == -40.0);
  }
  ```

  Kompilieren wie oben – doctest erzeugt dann eine eigene `main()`.
  (Alternativ: Catch2 mit `Catch2/catch.hpp` – gleiche Idee.)
- **`assert` abschalten:** Mit `-DNDEBUG` beim Kompilieren werden alle
  `assert`-Zeilen entfernt. Gut zu wissen – verwirrt aber erstmal, wenn dein
  „fehlerhafter“ Test plötzlich grün ist.

## Erweiterung (Bonus)

- Parametrisiere mit einem `std::vector` von Testdaten:

  ```cpp
  struct Fall { double eingabe; double erwartet; };
  std::vector<Fall> faelle = {{0.0, 32.0}, {100.0, 212.0}, {-40.0, -40.0}};
  for (const auto& f : faelle) {
      assert(celsius_nach_fahrenheit(f.eingabe) == f.erwartet);
  }
  ```

- Baue einen **Mutationstest**: Ändere `* 9.0 / 5.0` absichtlich zu
  `* 5.0 / 9.0` und prüfe, dass mindestens ein Test fehlschlägt. Danach
  zurückbauen.
- Teste die Kelvin-Umrechnung (falls in Lernfeld 1 als Bonus gebaut).

## Selbsttest

- [ ] `test_temperatur.cpp` existiert mit mindestens 6 Testfällen
- [ ] Kompiliert fehlerfrei mit `-std=c++17 -Wall -Wextra` (null Warnungen)
- [ ] `./test_temperatur` läuft ohne Abbruch durch (`echo $?` → `0`)
- [ ] Ein absichtlich eingebauter Fehler lässt mindestens einen Test fehlschlagen
- [ ] float-Vergleiche nutzen eine Toleranz (kein `==` auf `98.6`)

---

**Weiter:** [`aufgabe_02.md`](aufgabe_02.md)
