# Aufgabe 4: Klassen-Projekt – Bibliothekssystem (C++)

**Schwierigkeit:** ⭐⭐⭐ · **Themen:** mehrere Klassen, `std::vector<Buch>`, Referenzen `&`, `const`, Range-for

> 📄 Die Aufgabenstellung ist dieselbe wie in Python – lies dort zuerst die
> **Lernziele** und das **Beispiel**: [`../python/aufgaben/aufgabe_04.md`](../python/aufgaben/aufgabe_04.md)

## Aufgabenstellung (Kurzfassung)

Klasse `Buch` (`titel`, `autor`, `jahr`, `print() const`), Klasse `Bibliothek`
mit `std::vector<Buch> buecher;`, `hinzufuegen(const Buch& b)`,
`suche_nach_titel(const std::string&) const` (Teilstring, Groß-/Kleinschreibung
ignorieren) und `alle_anzeigen() const`. Menü: 1 hinzufügen · 2 suchen ·
3 alle anzeigen · 0 beenden.

## C++-spezifische Hinweise

- **Zwei Klassen, getrennt deklarieren:** `Bibliothek` kann `Buch` direkt
  nutzen, solange `Buch` **vorher** definiert ist – die Reihenfolge der
  Definitionen zählt!
- **Speicherung:** `std::vector<Buch>` speichert **Kopien**. `hinzufuegen`
  nimmt das Buch als `const Buch&` (Referenz, keine weitere Kopie) und legt
  eine Kopie im Vektor ab:

  ```cpp
  void Bibliothek::hinzufuegen(const Buch& b) {
      buecher.push_back(b);
  }
  ```

  In Python hattest du Referenzen in der Liste – in C++ ist es eine Kopie.
  Für kleine Objekte wie `Buch` völlig ok; für große Objekte nimmt man
  später `std::unique_ptr` (siehe Aufgabe 3).
- **Suche mit `const` + Referenz:**

  ```cpp
  std::vector<Buch> Bibliothek::suche_nach_titel(
      const std::string& suchbegriff) const {
      std::vector<Buch> treffer;
      for (const Buch& b : buecher) {
          if (b.titel.find(suchbegriff) != std::string::npos) {
              treffer.push_back(b);
          }
      }
      return treffer;
  }
  ```

  `const std::string&` = lesend, keine Kopie. Die Methode ist `const`, weil
  sie die Bibliothek nicht verändert. `std::string::npos` heißt „nicht
  gefunden".
- **Groß-/Kleinschreibung ignorieren:** C++ kann das nicht so elegant wie
  Pythons `lower()`. Einfacher Weg: beide Strings vor dem Vergleich klein
  schreiben:

  ```cpp
  #include <cctype>

  std::string klein(std::string s) {      // Wert-Parameter = eigene Kopie
      for (char& c : s) {
          c = std::tolower(static_cast<unsigned char>(c));
      }
      return s;
  }
  ```

  Dann: `klein(b.titel).find(klein(suchbegriff))`.
- **Nummerierte Ausgabe** mit Zähler:

  ```cpp
  int nr = 1;
  for (const Buch& b : buecher) {
      std::cout << "  " << nr++ << ". ";
      b.print();
  }
  ```

- **Menü & Eingabevalidierung** wie in Lernfeld 1, Aufgabe 2
  (`std::cin.fail()`).
- **Klassiker-Falle beim Jahr:** Nach `std::getline` für den Titel den Rest
  der Zeile verwerfen (`std::cin.ignore(...)`), sonst überspringt das nächste
  `std::getline` die Eingabe!

## Erweiterung (Bonus)

- `suche_nach_autor(const std::string&) const` analog zur Titelsuche.
- **Ausleihe:** `bool ausgeliehen;` in `Buch` + `ausleihen()`/`zurueckgeben()`;
  die Anzeige markiert ausgeliehene Bücher mit „(ausgeliehen)".
- **Datei-Speicherung:** `buecher.txt` schreiben und laden (`std::ifstream` /
  `std::ofstream`, `#include <fstream>`) – ein Buch pro Zeile, Felder mit `;`
  getrennt.

## Selbsttest

- [ ] `Buch` und `Bibliothek` sind getrennte Klassen
- [ ] Bücher lassen sich über das Menü hinzufügen
- [ ] Titelsuche findet Teilstrings (Groß-/Kleinschreibung egal)
- [ ] „Keine Treffer"-Fall wird sauber behandelt
- [ ] `alle_anzeigen()` nummeriert korrekt
- [ ] Ungültige Jahreszahl stürzt nicht ab
- [ ] Kompiliert fehlerfrei mit `-std=c++17 -Wall -Wextra` (null Warnungen)

---

**Weiter:** [`aufgabe_05.md`](aufgabe_05.md)
