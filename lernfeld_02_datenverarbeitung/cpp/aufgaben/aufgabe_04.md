# Aufgabe 4: Wortfrequenz-Analyse (C++)

**Schwierigkeit:** ⭐⭐⭐ · **Themen:** `std::ifstream`, `std::map<std::string, int>`, `std::vector`, `std::sort` mit Lambda

> 📄 Die Aufgabenstellung ist dieselbe wie in Python – lies dort zuerst
> **Lernziele** und **Beispiel**: [`../python/aufgaben/aufgabe_04.md`](../python/aufgaben/aufgabe_04.md)

## Aufgabenstellung (Kurzfassung)

`text.txt` einlesen, Wörter zählen (**Groß-/Kleinschreibung ignorieren**),
Anzahl der unterschiedlichen Wörter und **Top-5-Ranking** ausgeben.

## C++-spezifische Hinweise

- **Includes:** `<fstream>`, `<map>`, `<vector>`, `<string>`, `<cctype>`,
  `<algorithm>`, `<iostream>`.
- **Wörter einlesen – C++ kann das fast von allein:** `>>` liest
  **wortweise** und überspringt Leerzeichen und Zeilenumbrüche:

  ```cpp
  std::ifstream datei("text.txt");
  if (!datei.is_open()) {
      std::cout << "Datei text.txt nicht gefunden!" << std::endl;
      return 1;
  }
  std::map<std::string, int> zaehler;
  std::string wort;
  while (datei >> wort) {
      zaehler[klein(wort)]++;
  }
  ```

  ⚠️ **Satzzeichen:** `>>` lässt `.` `,` `!` `?` am Wort hängen – `sprache.`
  und `sprache` wären dann zwei verschiedene Wörter, und dein Ergebnis wiche
  vom Python-Beispiel ab. Entferne sie deshalb beim Einlesen – aber nur die
  **konkreten Zeichen**, nicht `ispunct()`: das würde auch das `+` aus
  „C++" entfernen!

  ```cpp
  while (!wort.empty() &&
         std::string(".,!?;:").find(wort.back()) != std::string::npos) {
      wort.pop_back();
  }
  ```
- **Kleinschreiben** – Pendant zu `wort.lower()`:

  ```cpp
  #include <cctype>
  std::string klein(const std::string& s) {
      std::string ergebnis;
      for (char c : s) {
          ergebnis += std::tolower(static_cast<unsigned char>(c));
      }
      return ergebnis;
  }
  ```

  Das `static_cast<unsigned char>` vermeidet undefiniertes Verhalten bei
  negativen `char`-Werten – ein bekanntes `-Wall`-Thema.
- **`std::map` sortiert automatisch nach Schlüssel** – praktisch, aber fürs
  Ranking brauchst du die Sortierung nach **Häufigkeit**. Trick: Paare in
  einen Vector kopieren und mit **Lambda** sortieren:

  ```cpp
  std::vector<std::pair<std::string, int>> eintraege(zaehler.begin(), zaehler.end());
  std::sort(eintraege.begin(), eintraege.end(),
            [](const auto& a, const auto& b) { return a.second > b.second; });
  ```

  Das Lambda vergleicht nur die Häufigkeit (`second`). `const auto&` spart dir
  das Ausschreiben der Typen.
- **Top 5 ausgeben:**

  ```cpp
  for (int i = 0; i < 5 && i < static_cast<int>(eintraege.size()); i++) {
      std::cout << (i + 1) << ". " << eintraege[i].first
                << " (" << eintraege[i].second << "×)" << std::endl;
  }
  ```

- **`++` statt `+ 1`:** `zaehler[wort]++` ist das Pendant zu Pythons
  `zaehler.get(wort, 0) + 1` – `operator[]` legt fehlende Schlüssel
  automatisch mit 0 an.

## Erweiterung (Bonus)

- **Stoppwörter** ignorieren („der", „die", „das", „und", „ist", „ein" …) –
  vor dem Zählen per `std::find` in einer Stoppwort-Liste prüfen.
- Balken-Diagramm: `std::string(eintraege[i].second, '#')` erzeugt n
  `#`-Zeichen.
- Komplettes Ranking in `ranking.txt` schreiben (`std::ofstream`).
- **Sätze zählen** (`.`, `!`, `?` im Text zählen) – oder eine eigene
  Zerlege-Funktion bauen, die Wörter auch über Kommas hinweg sauber trennt
  (wie in Lernfeld 1, Aufgabe 5).

## Selbsttest

- [ ] Alle Wörter der Datei werden gezählt
- [ ] „Python" und „python" zählen als ein Wort
- [ ] Die Top-5-Ausgabe ist nach Häufigkeit sortiert
- [ ] Weniger als 5 unterschiedliche Wörter stürzen das Programm nicht ab
- [ ] Fehlende Datei erzeugt eine saubere Meldung
- [ ] Kompiliert fehlerfrei mit `-std=c++17 -Wall -Wextra` (null Warnungen)

---

**Weiter:** [`aufgabe_05.md`](aufgabe_05.md)
