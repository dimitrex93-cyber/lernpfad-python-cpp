# Aufgabe 2: Temperaturumrechner (C++)

**Schwierigkeit:** ⭐⭐ · **Themen:** `while`-Schleife, Menü, Funktionen, `std::cin.fail()`, Formatierung

> 📄 Die Aufgabenstellung ist dieselbe wie in Python – lies dort zuerst
> **Lernziele** und **Beispiel**: [`../python/aufgaben/aufgabe_02.md`](../python/aufgaben/aufgabe_02.md)

## Aufgabenstellung (Kurzfassung)

Menü: **1** Celsius→Fahrenheit · **2** Fahrenheit→Celsius · **0** Beenden.
Schleife bis „0". Ungültige Eingaben abfangen – kein Absturz.

## C++-spezifische Hinweise

- **Funktionen mit Typen:**

  ```cpp
  double celsius_nach_fahrenheit(double c) {
      return c * 9.0 / 5.0 + 32.0;
  }
  ```

  ⚠️ Schreib `9.0` statt `9` – sonst passiert Ganzzahl-Division! (In Python
  wäre `9` kein Problem, in C++ schon – der klassische Denkfehler beim Wechsel.)
- **Formatierung auf 2 Nachkommastellen** (wie Pythons `:.2f`):

  ```cpp
  #include <iomanip>
  std::cout << std::fixed << std::setprecision(2) << wert << " °F" << std::endl;
  ```

  `std::fixed` setzt die feste Nachkommastellen-Anzeige, `std::setprecision(2)`
  auf 2 Stellen. Beides gilt danach **dauerhaft** für den Ausgabestrom – gut
  für dieses Programm, ein Stolperstein für spätere.
- **Eingabevalidierung** – das Pendant zu Pythons `try`/`except`:

  ```cpp
  double wert;
  std::cin >> wert;
  if (std::cin.fail()) {
      std::cin.clear();                                   // Fehlerzustand löschen
      std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
      std::cout << "Bitte eine Zahl eingeben." << std::endl;
      continue;
  }
  ```

  Dafür brauchst du `#include <limits>`.
- **Menü-Wahl:** `int wahl; std::cin >> wahl;` – prüfe `wahl == 1`, `wahl == 2`,
  `wahl == 0`. Für alles andere: Meldung + `continue`.

## Erweiterung (Bonus)

- Zusätzlich **Kelvin** (Menüpunkt 3): `K = C + 273.15`.
- Zähle die Umrechnungen und zeige die Zahl beim Beenden.
- Akzeptiere Eingaben wie `20C` oder `68F` direkt (Tipp: `std::string` einlesen,
  letztes Zeichen prüfen, Rest mit `std::stod()` umwandeln – Achtung: `stod`
  wirft eine Exception bei Müll, das fängt man mit `try`/`catch`).

## Selbsttest

- [ ] Beide Umrechnungsrichtungen liefern korrekte Ergebnisse
- [ ] Menü lässt sich mit „0" beenden
- [ ] Ungültige Menü-Wahl stürzt das Programm nicht ab
- [ ] Ungültiger Temperaturwert („abc") stürzt das Programm nicht ab
- [ ] Ausgabe hat genau 2 Nachkommastellen
- [ ] Kompiliert fehlerfrei mit `-std=c++17 -Wall -Wextra` (null Warnungen)

---

**Weiter:** [`aufgabe_03.md`](aufgabe_03.md)
