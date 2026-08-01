# Aufgabe 1: Zahlenstatistik aus einer Datei (C++)

**Schwierigkeit:** ⭐⭐ · **Themen:** `std::ifstream`, `std::vector<int>`, `std::min_element`/`std::max_element`, Ganzzahl-Division

> 📄 Die Aufgabenstellung ist dieselbe wie in Python – lies dort zuerst
> **Lernziele** und **Beispiel**: [`../python/aufgaben/aufgabe_01.md`](../python/aufgaben/aufgabe_01.md)

## Aufgabenstellung (Kurzfassung)

`zahlen.txt` einlesen (eine Zahl pro Zeile) und ausgeben: **Anzahl**,
**Minimum**, **Maximum**, **Durchschnitt** (1 Nachkommastelle). Fehlende Datei
→ saubere Meldung.

## C++-spezifische Hinweise

- **Includes:** `#include <fstream>` (Datei-Ein-/Ausgabe), `#include <vector>`,
  `#include <iostream>`, `#include <algorithm>` (für `min_element`).
- **Datei öffnen und prüfen:**

  ```cpp
  std::ifstream datei("zahlen.txt");
  if (!datei.is_open()) {
      std::cout << "Datei zahlen.txt nicht gefunden!" << std::endl;
      return 1;
  }
  ```

  `return 1;` meldet dem Betriebssystem einen Fehler (0 = Erfolg).
- **Zahlen einlesen – die idiomatische C++-Leseschleife:**

  ```cpp
  std::vector<int> zahlen;
  int wert;
  while (datei >> wert) {
      zahlen.push_back(wert);
  }
  ```

  `datei >> wert` liefert `false`, sobald das Dateiende erreicht ist. Das
  Pendant zu Pythons `for zeile in datei:` – aber hier liest C++ gleich als
  `int`, kein `int(...)`-Cast nötig.
- **Min/Max:** selbst mit Schleife oder bequem mit `<algorithm>` – Achtung,
  es kommt ein **Iterator** zurück, daher das `*`:

  ```cpp
  int minimum = *std::min_element(zahlen.begin(), zahlen.end());
  int maximum = *std::max_element(zahlen.begin(), zahlen.end());
  ```

- **Durchschnitt – Ganzzahl-Division!** `summe / zahlen.size()` wäre
  `int / int` und schneidet den Rest ab. Rechne so:

  ```cpp
  double durchschnitt = summe / static_cast<double>(zahlen.size());
  ```

  (In Python ergibt `/` automatisch eine Kommazahl – in C++ musst du den
  `double`-Cast **selbst** machen. Der klassische Denkfehler beim Wechsel!)
- **Formatierung auf 1 Nachkommastelle** (`#include <iomanip>`):

  ```cpp
  std::cout << std::fixed << std::setprecision(1) << durchschnitt << std::endl;
  ```

- **Leere Datei:** `zahlen.size() == 0` → vor der Berechnung prüfen und eine
  Meldung ausgeben – sonst Division durch 0!

## Erweiterung (Bonus)

- Zusätzlich **Median** (mittlerer Wert – Tipp: Vektor vorher mit
  `std::sort` sortieren) und **Spannweite** (max − min).
- Kommentarzeilen (`#`) und leere Zeilen überspringen (Tipp: mit
  `std::getline` Zeile für Zeile lesen und parsen).
- Statistik in `statistik.txt` schreiben (`std::ofstream` aus `<fstream>`).

## Selbsttest

- [ ] Alle Zahlen werden eingelesen
- [ ] Anzahl, Minimum, Maximum und Durchschnitt sind korrekt
- [ ] Durchschnitt hat genau 1 Nachkommastelle (keine Ganzzahl-Division!)
- [ ] Fehlende Datei erzeugt eine saubere Meldung (kein Absturz)
- [ ] Leere Datei erzeugt keine Division durch 0
- [ ] Kompiliert fehlerfrei mit `-std=c++17 -Wall -Wextra` (null Warnungen)

---

**Weiter:** [`aufgabe_02.md`](aufgabe_02.md)
