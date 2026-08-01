# Aufgabe 1: Persönliche Begrüßung (C++)

**Schwierigkeit:** ⭐ · **Themen:** `std::cin`/`std::cout`, Variablen, Typen, `std::string`

> 📄 Die Aufgabenstellung ist dieselbe wie in Python – lies dort zuerst die
> **Lernziele** und das **Beispiel**: [`../python/aufgaben/aufgabe_01.md`](../python/aufgaben/aufgabe_01.md)

## Aufgabenstellung (Kurzfassung)

Frage nach **Name** und **Geburtsjahr**, berechne das Alter
(`aktuelles_jahr − geburtsjahr`) und gib eine persönliche Begrüßung aus.

## C++-spezifische Hinweise

- **Includes:** `#include <iostream>` (Ein-/Ausgabe) und `#include <string>`
  (Texte) – beides zwingend nötig.
- **Eingabe Name:** Mit `>>` liest `std::cin` nur bis zum ersten Leerzeichen –
  für den vollen Namen („Anna Müller") nimm `std::getline(std::cin, name);`.
- **Eingabe Geburtsjahr:** `int geburtsjahr; std::cin >> geburtsjahr;` – hier
  wandelt C++ automatisch in `int` um. (Die Fehlerbehandlung für falsche
  Eingaben lernst du in Aufgabe 2.)
- **Aktuelles Jahr automatisch** holen (statt fest verdrahten):

  ```cpp
  #include <ctime>
  std::time_t jetzt = std::time(nullptr);
  std::tm* lokal = std::localtime(&jetzt);
  int aktuelles_jahr = lokal->tm_year + 1900;
  ```

  Das ist eine der wenigen Stellen, an denen C++-Code **unbequemer** als Python
  ist – `datetime.date.today().year` ist schöner. Gutes Beispiel für den
  Sprachvergleich!
- **Ausgabe:** `std::cout << "Hallo " << name << "!" << std::endl;` – jeder Wert
  wird einzeln mit `<<` angehängt.
- **`const` nutzen:** `aktuelles_jahr` ändert sich nie → `const int`.

## Erweiterung (Bonus)

- Gib die **ungefähren Lebenstage** aus (`alter * 365`).
- Prüfe, ob das Geburtsjahr in der Zukunft liegt, und gib eine freche Meldung aus.
- Achtung bei der Zukunft-Prüfung: Vergiss nicht `#include <ctime>`.

## Selbsttest

- [ ] Das Programm fragt Name und Geburtsjahr ab
- [ ] Auch Namen mit Leerzeichen („Anna Müller") werden komplett eingelesen
- [ ] Die Ausgabe enthält Name und berechnetes Alter
- [ ] Kompiliert fehlerfrei mit `g++ -std=c++17 -Wall -Wextra` (null Warnungen)

---

**Weiter:** [`aufgabe_02.md`](aufgabe_02.md)
