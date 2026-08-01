# Aufgabe 4: Notizen als CSV exportieren (C++)

**Schwierigkeit:** ⭐⭐⭐ · **Themen:** `std::ofstream`, CSV-Export, `sqlite3_column_*()`, `std::replace`

> 📄 Die Aufgabenstellung ist dieselbe wie in Python – lies dort zuerst
> **Lernziele** und **Beispiel**: [`../python/aufgaben/aufgabe_04.md`](../python/aufgaben/aufgabe_04.md)

## Aufgabenstellung (Kurzfassung)

Alle Notizen aus `notizen.db` in `notizen.csv` schreiben: Kopfzeile
`id;titel;inhalt;erstellt_am`, danach eine Zeile pro Notiz, Felder mit `;`
getrennt. `;` und Zeilenumbrüche in Feldern bereinigen. Anzahl der
exportierten Notizen ausgeben.

## C++-spezifische Hinweise

- **Datei schreiben** – `std::ofstream` aus `<fstream>`:

  ```cpp
  #include <fstream>
  std::ofstream datei("notizen.csv");
  if (!datei) {
      std::cerr << "Datei nicht schreibbar!" << std::endl;
      return 1;
  }
  datei << "id;titel;inhalt;erstellt_am\n";
  // ... pro Notiz:
  datei << id << ";" << titel << ";" << inhalt << ";" << datum << "\n";
  datei.close();
  ```

  Der `<<`-Operator funktioniert mit `std::string` und `int` – kein
  `sprintf`-Gefummel nötig.
- **Spalten auslesen:** `sqlite3_column_int(stmt, 0)` für die ID,
  `sqlite3_column_text(stmt, 1)` für Texte – und wie in Aufgabe 2 mit
  `reinterpret_cast` in `std::string` umwandeln.
- **Felder säubern** – `std::replace` aus `<algorithm>` ersetzt alle
  Vorkommen in einem String:

  ```cpp
  #include <algorithm>
  std::string csv_feld(std::string text) {
      std::replace(text.begin(), text.end(), ';', ',');
      std::replace(text.begin(), text.end(), '\n', ' ');
      return text;
  }
  ```

- **Leere Tabelle:** erst `SELECT COUNT(*)` prüfen und „Keine Notizen zum
  Exportieren." melden (oder trotzdem mit Kopfzeile schreiben – entscheide
  dich und begründe).
- **Umlaute:** `ofstream` schreibt UTF-8 so, wie die Strings im Speicher
  liegen – solange dein Quellcode UTF-8 ist (er ist es), passt alles.

## Erweiterung (Bonus)

- Export **sortiert** (neueste zuerst).
- Zusätzlich `notizen_kurz.csv` mit nur `id` und `titel`.
- Schreibe die CSV mit Anführungszeichen-Quoting um Feldtrennzeichen herum
  (Stichwort RFC 4180) – eine kleine, eigene `quote()`-Funktion.

## Selbsttest

- [ ] `notizen.csv` enthält die Kopfzeile
- [ ] Eine Zeile pro Notiz, Semikolon-getrennt
- [ ] `;` im Inhalt bricht die Datei nicht
- [ ] Die exportierte Anzahl wird ausgegeben
- [ ] Die Datei lässt sich mit einem Texteditor sauber lesen
- [ ] Kompiliert mit `g++ -std=c++17 -Wall -Wextra export.cpp -o export -lsqlite3` (null Warnungen)

---

**Weiter:** [`aufgabe_05.md`](aufgabe_05.md)
