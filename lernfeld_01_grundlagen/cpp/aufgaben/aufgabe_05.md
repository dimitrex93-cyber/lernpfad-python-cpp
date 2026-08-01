# Aufgabe 5: Textanalyse (C++)

**Schwierigkeit:** ⭐⭐⭐ · **Themen:** `std::string`, `std::vector<std::string>`, `std::map`, Tokenizing

> 📄 Die Aufgabenstellung ist dieselbe wie in Python – lies dort zuerst
> **Lernziele** und **Beispiel**: [`../python/aufgaben/aufgabe_05.md`](../python/aufgaben/aufgabe_05.md)

## Aufgabenstellung (Kurzfassung)

Mehrzeiligen Text einlesen (Ende bei Zeile `ENDE`). Auswerten: Zeichen ohne
Leerzeichen, Wortzahl, Ø Wortlänge, häufigstes Wort, 3 längste Wörter.
Groß-/Kleinschreibung ignorieren.

## C++-spezifische Hinweise

- **Mehrzeilige Eingabe:**

  ```cpp
  std::vector<std::string> zeilen;
  std::string zeile;
  while (std::getline(std::cin, zeile)) {
      if (zeile == "ENDE") break;
      zeilen.push_back(zeile);
  }
  ```

- **Wörter zerlegen** – C++ hat kein `split()` wie Python. Schreib dir eine
  kleine Hilfsfunktion (das ist eine echte C++-Übung!):

  ```cpp
  std::vector<std::string> zerlege(const std::string& text) {
      std::vector<std::string> woerter;
      std::string aktuell;
      for (char c : text) {
          if (c == ' ' || c == ',' || c == '.' || c == '!' || c == '?') {
              if (!aktuell.empty()) { woerter.push_back(aktuell); aktuell.clear(); }
          } else {
              aktuell += c;
          }
      }
      if (!aktuell.empty()) woerter.push_back(aktuell);
      return woerter;
  }
  ```

  (Moderner und kürzer ginge es mit `std::istringstream` aus `<sstream>` –
  aber die Schleife oben zeigt, *was* dabei passiert. Beides ist eine gute Lösung!)
- **Kleinbuchstaben** für den Vergleich:

  ```cpp
  #include <cctype>
  std::string klein(const std::string& s) {
      std::string ergebnis;
      for (char c : s) ergebnis += std::tolower(static_cast<unsigned char>(c));
      return ergebnis;
  }
  ```

- **Häufigkeitszählung** – Pendant zu Pythons Dictionary: `std::map<std::string, int>`
  aus `<map>` (sortiert automatisch!) oder `std::unordered_map` (schneller).
  Zählen: `zaehler[wort]++;` – legt fehlende Einträge automatisch mit 0 an.
  Das häufigste Wort findet man, indem man das Map durchläuft und das Maximum
  merkt.
- **Längste Wörter:** Wörter in einem `std::vector` sammeln und mit
  `std::sort` + Lambda nach Länge sortieren (`#include <algorithm>`):

  ```cpp
  std::sort(woerter.begin(), woerter.end(),
            [](const std::string& a, const std::string& b) {
                return a.size() > b.size();
            });
  ```

  Für Duplikate gibt es `std::unique` (nach `std::sort`).
- **Zeichen zählen:** Über alle Zeilen laufen und jedes Zeichen zählen, das
  kein Leerzeichen ist.

## Erweiterung (Bonus)

- Ranking der 5 häufigsten Wörter mit `*`-Balken.
- **Stoppwörter** ignorieren („der", „die", „das", „und", „ist", „ein" …) –
  einfach vor dem Zählen per `std::find` in einer Stoppwort-Liste prüfen.
- Sätze zählen (`.`/`!`/`?` zählen).

## Selbsttest

- [ ] Mehrzeilige Eingabe endet zuverlässig bei `ENDE`
- [ ] Zeichenzahl ohne Leerzeichen stimmt
- [ ] Wortzahl stimmt
- [ ] Groß-/Kleinschreibung wird ignoriert („Python" = „python")
- [ ] Häufigstes Wort und die 3 längsten Wörter sind korrekt
- [ ] Leerer Text stürzt das Programm nicht ab
- [ ] Kompiliert fehlerfrei mit `-std=c++17 -Wall -Wextra` (null Warnungen)

---

**Fertig mit den Aufgaben!** Jetzt das [Mini-Projekt](../mini_projekt/README.md) –
und dann `checklist.md` abhaken.
