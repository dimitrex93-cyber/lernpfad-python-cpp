# Aufgabe 2: Bubble Sort selbst gebaut (C++)

**Schwierigkeit:** ⭐⭐ · **Themen:** `std::vector`, verschachtelte `for`-Schleifen, `std::swap`, Referenzen

> 📄 Die Aufgabenstellung ist dieselbe wie in Python – lies dort zuerst
> **Lernziele** und **Beispiel**: [`../python/aufgaben/aufgabe_02.md`](../python/aufgaben/aufgabe_02.md)

## Aufgabenstellung (Kurzfassung)

`[7, 2, 9, 1, 5]` mit **selbst geschriebenem Bubble Sort** aufsteigend sortieren
– **ohne** `std::sort`! Ausgabe **vorher/nachher**.

## C++-spezifische Hinweise

- **Includes:** `#include <vector>`, `#include <iostream>`, `#include <utility>`
  (für `std::swap`).
- **Vector anlegen:**

  ```cpp
  std::vector<int> zahlen = {7, 2, 9, 1, 5};
  ```

- **Größe:** `zahlen.size()` liefert `std::size_t` (**unsigned**) – die
  innere Schleife `for (int j = 0; j < n - 1 - i; j++)` funktioniert, wenn du
  `int n = zahlen.size();` setzt. Ohne diesen Umweg drohen Vergleiche zwischen
  `int` und `size_t` (Compiler-Warnung mit `-Wextra`!).
- **Tauschen** – das Pendant zur Python-Tupel-Zuweisung:

  ```cpp
  std::swap(zahlen[j], zahlen[j + 1]);
  ```

  (In Python: `zahlen[j], zahlen[j+1] = zahlen[j+1], zahlen[j]`. In C++ gibt es
  diese Mehrfach-Zuweisung nicht – `std::swap` erledigt das.)
- **Ausgabe des Vektors** – C++ hat kein `print(liste)`. Schreib dir eine
  kleine Hilfsfunktion:

  ```cpp
  void zeige(const std::vector<int>& v) {
      std::cout << "[";
      for (std::size_t i = 0; i < v.size(); i++) {
          if (i > 0) std::cout << ", ";
          std::cout << v[i];
      }
      std::cout << "]" << std::endl;
  }
  ```

  Das `&` in `const std::vector<int>&` ist eine **Referenz** – so wird der
  Vektor nicht kopiert. `const`, weil die Funktion ihn nicht ändert.
- **Sortierfunktion als eigene Funktion** – das `&` ist hier Pflicht, sonst
  sortierst du nur eine **Kopie** und der Aufrufer merkt nichts:

  ```cpp
  void bubble_sort(std::vector<int>& v) {
      // zwei verschachtelte Schleifen:
      // innen: if (v[j] > v[j + 1]) std::swap(v[j], v[j + 1]);
  }
  ```

- Kein `std::sort` verwenden – genau darum geht es. (Zum **Gegenprüfen** deines
  Ergebnisses ist `std::sort` natürlich erlaubt.)

## Erweiterung (Bonus)

- Nach jedem Durchlauf den aktuellen Stand ausgeben (siehe `zeige` oben).
- Vergleiche und Tausche zählen und am Ende ausgeben.
- Zahlen aus `zahlen.txt` einlesen (wie Aufgabe 1) und sortieren.

## Selbsttest

- [ ] Ausgabe vorher/nachher ist korrekt aufsteigend sortiert
- [ ] Kein `std::sort` im Sortierteil verwendet
- [ ] Negative Zahlen und Duplikate werden korrekt sortiert
- [ ] Leerer Vektor und Ein-Element-Vektor stürzen nicht ab
- [ ] Die Funktion verändert den Vektor des Aufrufers (Referenz `&`)
- [ ] Kompiliert fehlerfrei mit `-std=c++17 -Wall -Wextra` (null Warnungen)

---

**Weiter:** [`aufgabe_03.md`](aufgabe_03.md)
