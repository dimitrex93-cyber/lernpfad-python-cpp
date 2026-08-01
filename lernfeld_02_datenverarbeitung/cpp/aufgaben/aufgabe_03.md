# Aufgabe 3: Binäre Suche (C++)

**Schwierigkeit:** ⭐⭐⭐ · **Themen:** `std::vector`, `while`-Schleife, Indexberechnung, `int`-Division

> 📄 Die Aufgabenstellung ist dieselbe wie in Python – lies dort zuerst
> **Lernziele** und **Beispiel**: [`../python/aufgaben/aufgabe_03.md`](../python/aufgaben/aufgabe_03.md)

## Aufgabenstellung (Kurzfassung)

Funktion `binaere_suche(const std::vector<int>& v, int wert)`, die in einer
**sortierten** Liste den **Index** des Werts zurückgibt (oder `-1`). Test mit
`{1, 3, 5, 7, 9, 11, 13}` und Benutzereingabe.

## C++-spezifische Hinweise

- **Includes:** `#include <vector>`, `#include <iostream>`, `#include <limits>`
  (für die Eingabevalidierung).
- **Funktion – der Kern:**

  ```cpp
  int binaere_suche(const std::vector<int>& v, int wert) {
      if (v.empty()) return -1;
      int links = 0;
      int rechts = static_cast<int>(v.size()) - 1;
      while (links <= rechts) {
          int mitte = (links + rechts) / 2;
          if (v[mitte] == wert) return mitte;
          if (v[mitte] < wert) links = mitte + 1;
          else                 rechts = mitte - 1;
      }
      return -1;
  }
  ```

- **`v.size()` ist `std::size_t` (unsigned):** Ohne Cast wäre `v.size() - 1`
  bei leerem Vektor eine riesige Zahl statt `-1` – die Schleife liefe ewig.
  Deshalb: `if (v.empty())` zuerst, dann `static_cast<int>(v.size()) - 1`.
- **`mitte` berechnen:** `(links + rechts) / 2` ist `int / int` –
  **Ganzzahl-Division** – genau das wollen wir hier: einen ganzzahligen Index.
  In Python brauchtest du `//`; in C++ macht `/` das bei `int` automatisch.
  Achtung: Derselbe Mechanismus war in Aufgabe 1 beim Durchschnitt **falsch** –
  der Kontext entscheidet!
- **Eingabe des Suchwerts mit Validierung** (wie in Lernfeld 1):

  ```cpp
  int wert;
  std::cin >> wert;
  if (std::cin.fail()) {
      std::cin.clear();
      std::cin.ignore(std::numeric_limits<std::streamsize>::max(), '\n');
      std::cout << "Bitte eine Zahl eingeben." << std::endl;
      continue;
  }
  ```

- **Mehrere Suchen:** Schleife, die bei Eingabe von `q` bricht – oder eine
  feste Anzahl Suchvorgänge. Die Liste bleibt dabei konstant.

## Erweiterung (Bonus)

- Vergleiche zählen und ausgeben („Die Suche brauchte X Schritte").
- **Rekursive** Variante: `binaere_suche(v, wert, links, rechts)` ruft sich mit
  der halbierten Spanne selbst auf (Abbruch: `links > rechts`).
- Vergleich mit **linearer Suche** (von vorn durchlaufen) bei einer Liste mit
  100.000 Elementen – lass dir beide Suchzeiten ausgeben (Vorgeschmack auf
  Aufgabe 5).

## Selbsttest

- [ ] `binaere_suche({1, 3, 5, 7, 9}, 7)` liefert `3`
- [ ] Erstes und letztes Element (Index 0 bzw. 4) werden gefunden
- [ ] Nicht enthaltene Werte liefern `-1`
- [ ] Leerer Vektor liefert `-1` (kein `size_t`-Underflow!)
- [ ] Ungültige Benutzereingaben stürzen das Programm nicht ab
- [ ] Kompiliert fehlerfrei mit `-std=c++17 -Wall -Wextra` (null Warnungen)

---

**Weiter:** [`aufgabe_04.md`](aufgabe_04.md)
